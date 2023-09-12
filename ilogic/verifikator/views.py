from django.contrib import messages
from django.contrib.auth.models import Group
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.template.loader import render_to_string
from openpyxl import Workbook
import pandas as pd
import numpy as np
import uuid
import time
import random
import datetime

from tablib import Dataset

from klaim.filters import RegisterKlaimFaskesFilter
from klaim.models import (
    RegisterKlaim,
    DataKlaimCBG, KeteranganPendingDispute
)
from klaim.resources import DataKlaimCBGResource
from .filters import DataKlaimCBGFilter, DownloadDataKlaimCBGFilter
from .forms import (
    StatusRegisterKlaimForm,
    ImportDataKlaimForm,
    DataKlaimVerifikatorForm, FinalisasiVerifikatorForm, HitungDataKlaimForm, KeteranganPendingForm,
    STATUS_CHOICES_DATA_KLAIM_VERIFIKATOR
)
from user.decorators import permissions
from user.models import User
from klaim.choices import (
    StatusDataKlaimChoices,
    JenisPelayananChoices, StatusRegisterChoices, NamaJenisKlaimChoices
)
from .models import HitungDataKlaim
from .storages import TemporaryStorage
from collections import Counter
from .utils import pembagian_tugas


@login_required
@permissions(role=['verifikator'])
def daftar_register(request):
    queryset = RegisterKlaim.objects.filter(
        nomor_register_klaim__startswith=request.user.kantorcabang_set.all().first().kode_cabang).order_by('-tgl_aju')

    # filter
    myFilter = RegisterKlaimFaskesFilter(request.GET, queryset=queryset)
    queryset = myFilter.qs

    # pagination
    paginator = Paginator(queryset, 25)
    page_number = request.GET.get('page')
    queryset = paginator.get_page(page_number)

    context = {
        'register_list': queryset,
        'myFilter': myFilter,
    }

    # (DataKlaimCBG.objects.filter(register_klaim__nomor_register_klaim='020123080001',
    #                                    status=StatusDataKlaimChoices.PROSES).
    #  update(status=StatusDataKlaimChoices.LAYAK))

    return render(request, 'verifikator/daftar_register.html', context)


@login_required
@permissions(role=['verifikator'])
def detail_register(request, pk):
    kantor_cabang = request.user.kantorcabang_set.all().first()
    queryset = RegisterKlaim.objects.filter(
        nomor_register_klaim__startswith=kantor_cabang.kode_cabang)
    instance = queryset.get(id=pk)
    status_form = StatusRegisterKlaimForm(instance=instance)
    if request.method == 'POST' and request.POST.get('action') == 'update_status':
        status_form = StatusRegisterKlaimForm(instance=instance, data=request.POST)
        if instance.verifikator != request.user:
            return HttpResponse(content="Anda Tidak Memiliki Hak Akses, Harap Menghubungi Admin!", status=403)
        if status_form.is_valid():
            status_form.save()
            if instance.jenis_klaim.nama == NamaJenisKlaimChoices.CBG_SUSULAN or instance.jenis_klaim.nama == NamaJenisKlaimChoices.OBAT_SUSULAN:
                data_klaim = DataKlaimCBG.objects.filter(faskes=instance.faskes,
                                                         bupel=instance.bulan_pelayanan,
                                                         status=StatusDataKlaimChoices.PEMBAHASAN)
                for data_klaim in data_klaim:
                    data_klaim.register_klaim = instance
                    data_klaim.tgl_SLA = None
                    data_klaim.status = StatusDataKlaimChoices.PROSES
                    data_klaim.prosesklaim = False
                    data_klaim.is_hitung = False
                    data_klaim.save()
            messages.success(request, "Data Berhasil Disimpan. Selanjutnya lakukan import data klaim. Terima Kasih")
            return redirect(request.headers.get('Referer'))

    context = {
        'register': instance,
        'status_form': status_form
    }
    return render(request, 'verifikator/detail_register.html', context)


@login_required
@permissions(role=['verifikator'])
def import_data_klaim(request):
    storage = TemporaryStorage()
    import_form = ImportDataKlaimForm()
    verifikator = User.objects.filter(kantorcabang__in=request.user.kantorcabang_set.all(),
                                      groups__name='verifikator',
                                      is_active=True,
                                      is_staff=True)
    if request.method == 'POST' and request.POST.get('action') == 'import':
        import_form = ImportDataKlaimForm(files=request.FILES, data=request.POST)
        if import_form.is_valid():
            nomor_register_klaim = import_form.cleaned_data.get('register')
            register = RegisterKlaim.objects.get(nomor_register_klaim=nomor_register_klaim)
            file_name = f'{uuid.uuid4()}-{int(round(time.time() * 1000))}.xlsx'
            storage.save(name=file_name, content=import_form.cleaned_data.get('file'))
            data_frame = pd.read_excel(storage.path(name=file_name))
            data_frame = data_frame.replace(np.nan, None)
            data_frame['register_klaim'] = register
            data_frame['faskes'] = register.faskes
            data_frame['TGLPULANG'] = pd.to_datetime(data_frame['TGLPULANG'])
            data_frame['bupel'] = data_frame['TGLPULANG'].dt.to_period('M').dt.to_timestamp()
            data_frame['bupel'] = pd.to_datetime(data_frame['bupel'])

            with transaction.atomic():
                obj_list = DataKlaimCBG.objects.bulk_create(
                    [DataKlaimCBG(**dict(row[1])) for row in data_frame.iterrows()]
                )

                valid_data = DataKlaimCBG.objects.filter(id__in=[obj.id for obj in obj_list
                                                                 if obj.NOSEP[:8] == register.faskes.kode_ppk and
                                                                 obj.bupel.month == register.bulan_pelayanan.month and
                                                                 obj.bupel.year == register.bulan_pelayanan.year])
                invalid_data = DataKlaimCBG.objects.filter(id__in=[obj.id for obj in obj_list
                                                                   if obj.NOSEP[:8] != register.faskes.kode_ppk or
                                                                   obj.bupel.month != register.bulan_pelayanan.month or
                                                                   obj.bupel.year != register.bulan_pelayanan.year])

                df_valid = pd.DataFrame.from_records(valid_data.values())
                total_data_valid = len(df_valid)
                df_invalid = pd.DataFrame.from_records(invalid_data.values())
                total_data_invalid = len(df_invalid)
                transaction.set_rollback(True)
            return render(request, 'verifikator/preview_data_import.html',
                          {'preview_data_valid': df_valid,
                           'total_data_valid': total_data_valid,
                           'preview_data_invalid': df_invalid,
                           'total_data_invalid': total_data_invalid,
                           'file_name': file_name,
                           'register': nomor_register_klaim})

    if request.method == 'POST' and request.POST.get('action') == 'confirm':
        file_name = request.POST.get('file_name')
        nomor_register_klaim = request.POST.get('register')
        register = RegisterKlaim.objects.get(nomor_register_klaim=nomor_register_klaim)

        data_frame = pd.read_excel(storage.path(name=file_name))
        data_frame = data_frame.replace(np.nan, None)
        data_frame['register_klaim'] = register
        data_frame['faskes'] = register.faskes
        data_frame['TGLPULANG'] = pd.to_datetime(data_frame['TGLPULANG'])
        data_frame['bupel'] = data_frame['TGLPULANG'].dt.to_period('M').dt.to_timestamp()
        data_frame['bupel'] = pd.to_datetime(data_frame['bupel'])

        with transaction.atomic():
            register.has_import_data = True
            register.save()
            obj_list = DataKlaimCBG.objects.bulk_create(
                [DataKlaimCBG(**dict(row[1])) for row in data_frame.iterrows()]
            )

            # verifikator = register.faskes.kantor_cabang.user.filter(groups__name='verifikator')
            # queryset = DataKlaimCBG.objects.filter(register_klaim=register, status=StatusDataKlaimChoices.BELUM_VER)
            # NMPESERTA_RJ = [obj.NMPESERTA for obj in queryset.filter(JNSPEL=JenisPelayananChoices.RAWAT_JALAN)]
            #
            # list_nmpeserta_sort_freq = [item for items, c in Counter(NMPESERTA_RJ).most_common() for item in
            #                             [items] * c]
            # list_nmpeserta_no_duplicate = list(dict.fromkeys(list_nmpeserta_sort_freq))
            #
            # index = random.randrange(verifikator.count())
            # for i in range(len(list_nmpeserta_no_duplicate)):
            #     queryset.filter(NMPESERTA=list_nmpeserta_no_duplicate[i], JNSPEL=JenisPelayananChoices.RAWAT_JALAN). \
            #         update(verifikator=verifikator[index], status=StatusDataKlaimChoices.PROSES)
            #     if index == verifikator.count() - 1:
            #         index = 0
            #     else:
            #         index += 1

            # verifikator = register.faskes.kantor_cabang.user.filter(groups__name='verifikator',
            #                                                         is_active=True,
            #                                                         is_staff=True)
            # for i in verifikator_eksisting:
            #     get_verifikator = request.POST.get(str(i))
            #     if get_verifikator is not None:
            #         verifikator.append(get_verifikator)
            queryset = DataKlaimCBG.objects.filter(register_klaim=register, status=StatusDataKlaimChoices.BELUM_VER)

            NMPESERTA_RJ = [obj.NMPESERTA for obj in queryset.filter(JNSPEL=JenisPelayananChoices.RAWAT_JALAN)]
            list_nmpeserta_sort_freq_rawat_jalan = [item for items, c in Counter(NMPESERTA_RJ).most_common() for item in
                                                    [items] * c]
            list_nmpeserta_no_duplicate_rawat_jalan = list(dict.fromkeys(list_nmpeserta_sort_freq_rawat_jalan))

            index = random.randrange(len(verifikator))
            for i in range(len(list_nmpeserta_no_duplicate_rawat_jalan)):
                queryset.filter(NMPESERTA=list_nmpeserta_no_duplicate_rawat_jalan[i],
                                JNSPEL=JenisPelayananChoices.RAWAT_JALAN). \
                    update(verifikator=verifikator[index], status=StatusDataKlaimChoices.PROSES)
                if index == len(verifikator) - 1:
                    index = 0
                else:
                    index += 1
            # index = random.randrange(verifikator.count())
            # for obj in queryset.filter(JNSPEL=JenisPelayananChoices.RAWAT_INAP):
            #     obj.verifikator = verifikator[index]
            #     obj.status = StatusDataKlaimChoices.PROSES
            #     obj.save()
            #     if index == verifikator.count() - 1:
            #         index = 0
            #     else:
            #         index += 1
            NMPESERTA_RI = [obj.NMPESERTA for obj in queryset.filter(JNSPEL=JenisPelayananChoices.RAWAT_INAP)]
            list_nmpeserta_sort_freq_rawat_inap = [item for items, c in Counter(NMPESERTA_RI).most_common() for item in
                                                   [items] * c]
            list_nmpeserta_no_duplicate_rawat_inap = list(dict.fromkeys(list_nmpeserta_sort_freq_rawat_inap))

            index = random.randrange(len(verifikator))
            for i in range(len(list_nmpeserta_no_duplicate_rawat_inap)):
                queryset.filter(NMPESERTA=list_nmpeserta_no_duplicate_rawat_inap[i],
                                JNSPEL=JenisPelayananChoices.RAWAT_INAP). \
                    update(verifikator=verifikator[index], status=StatusDataKlaimChoices.PROSES)
                if index == len(verifikator) - 1:
                    index = 0
                else:
                    index += 1

            # sinkronisasi data
            q = DataKlaimCBG.objects.filter(register_klaim=register,
                                            status=StatusDataKlaimChoices.PROSES)
            for q in q:
                q.save()

            register.file_data_klaim = storage.open(name=file_name)
            register.file_data_klaim.name = file_name
            register.save()

    # if request.method == "POST" and request.POST.get("action") == "pembagian":
    #     register = get_object_or_404(RegisterKlaim, nomor_register_klaim=request.POST.get("register"))
    #     verifikator = register.faskes.kantor_cabang.user.filter(
    #         groups__name='verifikator', id__in=request.POST.getlist('verifikator'))
    #     old_register = RegisterKlaim.objects.filter(
    #         bulan_pelayanan__month=register.bulan_pelayanan.month,
    #         bulan_pelayanan__year=register.bulan_pelayanan.year,
    #         status='Selesai').exclude(nomor_register_klaim=register.nomor_register_klaim).last()
    #     queryset_dataklaim = DataKlaimCBG.objects.filter(register_klaim=old_register, status__in=['Pending', 'Dispute'],
    #                                                      register_klaim__jenis_klaim=old_register.jenis_klaim)
    #     queryset_id = [o.id for o in queryset_dataklaim]
    #     # print(queryset_id)
    #     # print('queryset_dataklaim:', queryset_dataklaim)
    #     with transaction.atomic():
    #         register.has_import_data = True
    #         register.file_data_klaim = 'done'
    #         register.save()
    #         queryset_dataklaim.update(register_klaim=register)
    #         pembagian_tugas(queryset_id=queryset_id, verifikator=verifikator)

    context = {
        'import_form': import_form,
        'verifikator': verifikator,
    }
    return render(request, 'verifikator/import_data_klaim.html', context)


@login_required
@permissions(role=['verifikator'])
def daftar_data_klaim(request):
    queryset = DataKlaimCBG.objects.filter(verifikator=request.user, prosesklaim=False).order_by('NMPESERTA', 'TGLSEP')

    # filter
    myFilter = DataKlaimCBGFilter(request.GET, queryset=queryset)
    queryset = myFilter.qs
    export = request.GET.get('export')
    if export == 'export':
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = 'attachment; filename={date}-dataverifikasi.xlsx'.format(
            date=datetime.datetime.now().strftime('%Y-%m-%d'),
        )
        workbook = Workbook()

        # Get active worksheet/tab
        worksheet = workbook.active
        worksheet.title = 'Data Klaim CBG'

        # Define the titles for columns
        columns = [
            'namars',
            'status',
            'NOSEP',
            'TGLSEP',
            'TGLPULANG',
            'JNSPEL',
            'NOKARTU',
            'NMPESERTA',
            'POLI',
            'KDINACBG',
            'BYPENGAJUAN',
            'verifikator',
            'ket_pending',
        ]
        row_num = 1

        # Assign the titles for each cell of the header
        for col_num, column_title in enumerate(columns, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = column_title

        # Iterate through all movies
        for queryset in queryset:
            row_num += 1

            # Define the data for each cell in the row
            row = [
                queryset.faskes.nama,
                queryset.status,
                queryset.NOSEP,
                queryset.TGLSEP,
                queryset.TGLPULANG,
                queryset.JNSPEL,
                queryset.NOKARTU,
                queryset.NMPESERTA,
                queryset.POLI,
                queryset.KDINACBG,
                queryset.BYPENGAJUAN,
                queryset.verifikator.first_name,
                # queryset.ket_pending_dispute,
            ]

            # Assign the data for each cell of the row
            for col_num, cell_value in enumerate(row, 1):
                cell = worksheet.cell(row=row_num, column=col_num)
                cell.value = cell_value

        workbook.save(response)
        return response
    if request.POST.get('import'):
        file = request.FILES['excel']
        df = pd.read_excel(file)

        # Call the Student Resource Model and make its instance
        data_claim_resource = DataKlaimCBGResource()

        # Load the pandas dataframe into a tablib dataset
        dataset = Dataset().load(df)

        try:
            result = data_claim_resource.import_data(dataset, dry_run=True, raise_errors=True)
            if not result.has_errors():
                # Impor data sebenarnya (setelah sukses dry_run)
                data_claim_resource.import_data(dataset, dry_run=False)
                messages.success(request, 'Data berhasil diimpor. {0} {1}'.format(dataset, data_claim_resource))
            else:
                # Ada kesalahan, tampilkan pesan kesalahan kepada pengguna
                messages.info(request, 'Terjadi kesalahan saat mengimpor data.')
        except Exception as e:
            # Nampilih error
            messages.info(request, f'Terjadi kesalahan: {str(e)}')
    # pagination
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    queryset = paginator.get_page(page_number)

    context = {
        'data_klaim': queryset,
        'myFilter': myFilter,
    }

    return render(request, 'verifikator/daftar_data_klaim.html', context)



@login_required
@permissions(role=['verifikator'])
def detail_data_klaim(request, pk):
    dataklaimcbg = DataKlaimCBG.objects.filter(verifikator=request.user).get(id=pk)
    listchoicestatus = STATUS_CHOICES_DATA_KLAIM_VERIFIKATOR
    context = {
        "dataklaimcbg": dataklaimcbg,
        "listchoicestatus": listchoicestatus,
    }
    return render(request, 'verifikator/detail_data_klaim.html', context)


# def edit_detail_data_klaim(request):
#     data = request.POST
#     if data.get('id_dataklaimcbg'):
#         dataklaimcbg = DataKlaimCBG.objects.get(id=data.get('id_dataklaimcbg'))
#
#         if dataklaimcbg.is_hitung is False:
#             add_hitung_data_klaim = HitungDataKlaim(nomor_register_klaim=dataklaimcbg.register_klaim.nomor_register_klaim,
#                                                 jenis_klaim=dataklaimcbg.register_klaim.jenis_klaim,
#                                                 verifikator=dataklaimcbg.verifikator)
#             add_hitung_data_klaim.save()
#             dataklaimcbg.is_hitung = True
#             dataklaimcbg.save()
#
#         keterangan = data.get('keterangan')
#         keterangan_pending_dispute = KeteranganPendingDispute(
#             ket_pending_dispute=keterangan
#         )
#         keterangan_pending_dispute.save()
#         dataklaimcbg.ket_pending_dispute.add(keterangan_pending_dispute)
#         dataklaimcbg.save()
#
#         next = request.POST.get('next', '/')
#         return HttpResponseRedirect(next)
#     else:
#         messages.info(request, "Hmmm sepertinya ada yang salah.")
#         return redirect('/')


@login_required
@permissions(role=['verifikator'])
def detail_data_klaim(request, pk):
    queryset = DataKlaimCBG.objects.filter(verifikator=request.user)
    instance = queryset.get(pk=pk)
    data_klaim_form = DataKlaimVerifikatorForm(instance=instance)
    data_klaim_pending_form = KeteranganPendingForm()

    if request.method == 'POST':
        data_klaim_form = DataKlaimVerifikatorForm(instance=instance, data=request.POST)
        keterangan = KeteranganPendingForm(request.POST or None)
        if data_klaim_form.is_valid():
            if instance.is_hitung is False:
                HitungDataKlaim.objects.create(nomor_register_klaim=instance.register_klaim.nomor_register_klaim,
                                               jenis_klaim=instance.register_klaim.jenis_klaim,
                                               verifikator=instance.verifikator)
                instance.is_hitung = True
                instance.save()
            if instance.status != StatusDataKlaimChoices.LAYAK:
                obj_keterangan = keterangan.save()
                obj_keterangan.verifikator = instance.verifikator
                obj_keterangan.save()
                instance.ket_pending_dispute.add(obj_keterangan)
            data_klaim_form.save()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

    context = {
        'data_klaim': instance,
        'data_klaim_form': data_klaim_form,
        'data_klaim_pending_form': data_klaim_pending_form,
    }
    return render(request, 'verifikator/detail_data_klaim.html', context)


@login_required
@permissions(role=['verifikator'])
def finalisasi_data_klaim(request):
    queryset = RegisterKlaim.objects.filter(
        nomor_register_klaim__startswith=request.user.kantorcabang_set.all().first().kode_cabang,
        status=StatusRegisterChoices.VERIFIKASI).order_by('created_at')

    # pagination
    paginator = Paginator(queryset, 25)
    page_number = request.GET.get('page')
    queryset = paginator.get_page(page_number)

    context = {
        'register_list': queryset,
    }

    return render(request, 'verifikator/finalisasi_data_klaim.html', context)


@login_required
@permissions(role=['verifikator'])
def update_finalisasi_data_klaim(request, pk):
    kantor_cabang = request.user.kantorcabang_set.all().first()
    queryset = RegisterKlaim.objects.filter(
        nomor_register_klaim__startswith=kantor_cabang.kode_cabang)
    instance = queryset.get(id=pk)

    # count
    data_klaim = DataKlaimCBG.objects.filter(register_klaim=instance)
    jumlah_proses = data_klaim.filter(status=StatusDataKlaimChoices.PROSES).count()
    jumlah_layak = data_klaim.filter(status=StatusDataKlaimChoices.LAYAK).count()
    jumlah_pending = data_klaim.filter(status=StatusDataKlaimChoices.PENDING).count()
    jumlah_dispute = data_klaim.filter(status=StatusDataKlaimChoices.DISPUTE).count()
    jumlah_tidak_layak = data_klaim.filter(status=StatusDataKlaimChoices.TIDAK_LAYAK).count()
    jumlah_klaim = data_klaim.filter(status=StatusDataKlaimChoices.KLAIM).count()
    total_klaim = data_klaim.count()

    # biaya
    biaya_proses = data_klaim.filter(status=StatusDataKlaimChoices.PROSES).aggregate(Sum('BYPENGAJUAN'))[
        'BYPENGAJUAN__sum']
    biaya_layak = data_klaim.filter(status=StatusDataKlaimChoices.LAYAK).aggregate(Sum('BYPENGAJUAN'))[
        'BYPENGAJUAN__sum']
    biaya_pending = data_klaim.filter(status=StatusDataKlaimChoices.PENDING).aggregate(Sum('BYPENGAJUAN'))[
        'BYPENGAJUAN__sum']
    biaya_dispute = data_klaim.filter(status=StatusDataKlaimChoices.DISPUTE).aggregate(Sum('BYPENGAJUAN'))[
        'BYPENGAJUAN__sum']
    biaya_tidak_layak = data_klaim.filter(status=StatusDataKlaimChoices.TIDAK_LAYAK).aggregate(Sum('BYPENGAJUAN'))[
        'BYPENGAJUAN__sum']
    biaya_klaim = data_klaim.aggregate(Sum('BYPENGAJUAN'))['BYPENGAJUAN__sum']

    status_form = FinalisasiVerifikatorForm(instance=instance)
    if request.method == 'POST' and request.POST.get('action') == 'update_status':
        status_form = FinalisasiVerifikatorForm(instance=instance, data=request.POST)
        if instance.verifikator != request.user:
            return HttpResponse(content="Anda Tidak Memiliki Hak Akses, Harap Menghubungi Admin!", status=403)
        if instance.sisa_klaim > 0:
            messages.warning(request, "Tidak dapat difinalisasi! Masih ada sisa klaim yang belum diverifikasi. "
                                      "Terima Kasih.")
        elif status_form.is_valid() and instance.sisa_klaim == 0:
            status_form.save()
            if instance.is_final is False:
                instance.is_final = True
                instance.save()
            data_klaim.filter(status=StatusDataKlaimChoices.LAYAK).update(status=StatusDataKlaimChoices.KLAIM)
            data_klaim.filter(status=StatusDataKlaimChoices.PENDING).update(prosespending=True)
            data_klaim.filter(status=StatusDataKlaimChoices.DISPUTE).update(prosespending=True, prosesdispute=True)
            data_klaim.update(prosesklaim=True)
            messages.success(request, "Register dan Data Klaim berhasil difinalisasi. Terima Kasih.")
            return redirect(request.headers.get('Referer'))

    context = {
        'register': instance,
        'status_form': status_form,
        'jumlah_proses': jumlah_proses,
        'jumlah_layak': jumlah_layak,
        'jumlah_pending': jumlah_pending,
        'jumlah_dispute': jumlah_dispute,
        'jumlah_tidak_layak': jumlah_tidak_layak,
        'jumlah_klaim': jumlah_klaim,
        'total_klaim': total_klaim,
        'biaya_proses': biaya_proses,
        'biaya_layak': biaya_layak,
        'biaya_pending': biaya_pending,
        'biaya_dispute': biaya_dispute,
        'biaya_tidak_layak': biaya_tidak_layak,
        'biaya_klaim': biaya_klaim,
    }
    return render(request, 'verifikator/update_finalisasi_data_klaim.html', context)


@login_required
@permissions(role=['verifikator'])
def update_data_klaim_cbg(request, pk):
    data = dict()
    data_klaim = get_object_or_404(DataKlaimCBG, id=pk)

    if request.method == 'POST':
        form = DataKlaimVerifikatorForm(request.POST, instance=data_klaim)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = DataKlaimVerifikatorForm(instance=data_klaim)
    context = {
        'form': form,
        'data_klaim': data_klaim,
    }
    data['html_form'] = render_to_string(request=request, template_name='verifikator/update_data_klaim.html',
                                         context=context)
    return JsonResponse(data)


@login_required
@permissions(role=['verifikator'])
def download_data_cbg(request):
    # initial relasi pada kantor cabang
    related_kantor_cabang = request.user.kantorcabang_set.all()
    queryset = DataKlaimCBG.objects.filter(verifikator__kantorcabang__in=related_kantor_cabang)

    # filter
    myFilter = DownloadDataKlaimCBGFilter(request.GET, queryset=queryset)
    queryset = myFilter.qs

    kantor_cabang = request.user.kantorcabang_set.all().first()
    DownloadDataKlaimCBGFilter.fields['verifikator'].queryset = kantor_cabang.user.filter(
        groups__in=Group.objects.filter(name='verifikator'), is_active=True, is_staff=True)


    # fitur download
    download = request.GET.get('download')
    if download == 'download':
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = 'attachment; filename={date}-dataverifikasi.xlsx'.format(
            date=datetime.datetime.now().strftime('%Y-%m-%d'),
        )
        workbook = Workbook()

        # Get active worksheet/tab
        worksheet = workbook.active
        worksheet.title = 'Data Klaim CBG'

        # Define the titles for columns
        columns = [
            'namars',
            'status',
            'NOSEP',
            'TGLSEP',
            'TGLPULANG',
            'JNSPEL',
            'NOKARTU',
            'NMPESERTA',
            'POLI',
            'KDINACBG',
            'BYPENGAJUAN',
            'verifikator',
            'ket_pending',
        ]
        row_num = 1

        # Assign the titles for each cell of the header
        for col_num, column_title in enumerate(columns, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = column_title

        # Iterate through all movies
        for queryset in queryset:
            row_num += 1

            # Define the data for each cell in the row
            row = [
                queryset.faskes.nama,
                queryset.status,
                queryset.NOSEP,
                queryset.TGLSEP,
                queryset.TGLPULANG,
                queryset.JNSPEL,
                queryset.NOKARTU,
                queryset.NMPESERTA,
                queryset.POLI,
                queryset.KDINACBG,
                queryset.BYPENGAJUAN,
                queryset.verifikator.first_name,
                # queryset.ket_pending_dispute,
            ]

            # Assign the data for each cell of the row
            for col_num, cell_value in enumerate(row, 1):
                cell = worksheet.cell(row=row_num, column=col_num)
                cell.value = cell_value

        workbook.save(response)
        return response

    context = {
        'myFilter': myFilter,
    }
    return render(request, 'verifikator/download_data_cbg.html', context)