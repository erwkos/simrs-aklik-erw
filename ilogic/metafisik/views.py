import datetime
import io
import random
import time
import uuid
import msoffcrypto
import numpy as np
import pandas as pd
import xlsxwriter
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction, IntegrityError
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from msoffcrypto.exceptions import InvalidKeyError, DecryptionError
from xlrd import XLRDError

from klaim.choices import JenisPelayananChoices, StatusDataKlaimChoices
from klaim.models import RegisterKlaim, DataKlaimCBG, SLA
from metafisik.filters import ListBAFilter
from metafisik.forms import ImportDataKlaimCBGMetafisikForm
from metafisik.fungsi import export_data_klaim, distribute_claims_to_verifikator
from metafisik.models import DataKlaimCBGMetafisik, NoBAMetafisik
from user.decorators import check_device, permissions
from user.models import User
from verifikator.storages import TemporaryStorage


@login_required
@check_device
@permissions(role=['supervisorkp'])
def list_no_ba_cbg_metafisik_kp(request):
    queryset = NoBAMetafisik.objects.all().order_by('-created_at')

    # filter
    myFilter = ListBAFilter(request.GET, queryset=queryset)
    queryset = myFilter.qs

    # pagination
    paginator = Paginator(queryset, 25)
    page_number = request.GET.get('page')
    queryset = paginator.get_page(page_number)

    export = request.GET.get('export')
    no_bast_export = request.GET.get('no_bast_export')
    try:
        if export == 'export':
            return export_data_klaim(no_bast_export)
    except Exception as e:
        messages.warning(request, f"Terjadi kesalahan pada saat ekspor data. Keterangan error : {e}")
        return redirect(request.headers.get('referer'))

    context = {
        'list_no_ba': queryset,
        'myFilter': myFilter,
    }
    return render(request, 'metafisik/list_no_ba_cbg_metafisik.html', context)


@login_required
@check_device
@permissions(role=['verifikator', 'supervisor'])
def list_no_ba_cbg_metafisik(request):
    kantor_cabang = request.user.kantorcabang_set.all().first().kode_cabang
    queryset = NoBAMetafisik.objects.filter(kdkclayan=kantor_cabang).order_by('-created_at')
    verifikator = User.objects.filter(kantorcabang__in=request.user.kantorcabang_set.all(),
                                      groups__name='verifikator',
                                      is_active=True,
                                      is_staff=True)

    # filter
    myFilter = ListBAFilter(request.GET, queryset=queryset)
    queryset = myFilter.qs

    # pagination
    paginator = Paginator(queryset, 25)
    page_number = request.GET.get('page')
    queryset = paginator.get_page(page_number)

    bagi = request.POST.get('bagi')
    if request.method == 'POST' and bagi == 'bagi':
        no_surat_bast = request.POST.get('no_surat_bast')
        cek_register_klaim = RegisterKlaim.objects.filter(no_ba_terima=no_surat_bast).exists()

        if not no_surat_bast:
            messages.warning(request, 'No Surat BAST tidak ditemukan dalam permintaan.')
            return redirect(request.headers.get('referer'))
        elif cek_register_klaim is False:
            messages.warning(request, f'No Surat BAST {no_surat_bast} tidak ada pada register klaim.')
            return redirect(request.headers.get('referer'))

        # Mendapatkan verifikator_list dengan filter yang ditentukan
        verifikator_list = list(verifikator)

        # Melanjutkan distribusi klaim dengan meneruskan verifikator_list
        success = distribute_claims_to_verifikator(no_surat_bast, verifikator_list)

        if success:
            messages.success(request, 'Klaim berhasil dibagi ke verifikator.')
        else:
            messages.warning(request, 'Terjadi kesalahan saat membagi klaim ke verifikator.')
        return redirect(request.headers.get('referer'))

    # Export data klaim
    export = request.GET.get('export')
    no_bast_export = request.GET.get('no_bast_export')
    if export == 'export':
        return export_data_klaim(no_bast_export)

    context = {
        'list_no_ba': queryset,
        'myFilter': myFilter,
        'verifikator': verifikator,
    }
    return render(request, 'metafisik/list_no_ba_cbg_metafisik.html', context)


@login_required
@check_device
@permissions(role=['supervisorkp'])
def import_no_ba_cbg_metafisik(request):
    storage = TemporaryStorage()
    import_form = ImportDataKlaimCBGMetafisikForm()
    if request.method == 'POST' and request.POST.get('action') == 'import':
        import_form = ImportDataKlaimCBGMetafisikForm(files=request.FILES, data=request.POST)
        if import_form.is_valid():
            list_data_import = ['No Surat Bast', 'Tgl Bast', 'Tgl Pelayanan', 'Kdkrlayan', 'Kdkclayan', 'Kdppklayan',
                                'Nmppklayan', 'Total Klaim']
            file_name = f'{uuid.uuid4()}-{int(round(time.time() * 1000))}.xlsx'
            storage.save(name=file_name, content=import_form.cleaned_data.get('file'))
            try:
                data_frame = pd.read_excel(storage.path(name=file_name), usecols=list_data_import)
                data_frame = data_frame.replace(np.nan, None)
                data_frame['Tgl Bast'] = pd.to_datetime(data_frame['Tgl Bast'])
                data_frame['Tgl Pelayanan'] = pd.to_datetime(data_frame['Tgl Pelayanan'])
                data_frame['Kdkclayan'] = data_frame['Kdkclayan'].astype('str').apply(lambda x: x.zfill(4))
                data_frame = data_frame.rename(columns={'No Surat Bast': 'no_surat_bast',
                                                        'Tgl Bast': 'tgl_bast',
                                                        'Tgl Pelayanan': 'tgl_pelayanan',
                                                        'Kdkrlayan': 'kdkrlayan',
                                                        'Kdkclayan': 'kdkclayan',
                                                        'Kdppklayan': 'kdppklayan',
                                                        'Nmppklayan': 'nmppklayan',
                                                        'Total Klaim': 'total_klaim',
                                                        })
            except Exception as e:
                messages.warning(request, f'Terjadi kesalahan pada saat import File. Keterangan error : {e}')
                return redirect(request.headers.get('Referer'))

            try:
                obj_list = []
                for _, row in data_frame.iterrows():
                    data_klaim = NoBAMetafisik()
                    try:
                        data_klaim = NoBAMetafisik(**dict(row))
                        data_klaim.full_clean()  # Validate the object
                        obj_list.append(data_klaim)
                    except Exception as e:
                        messages.warning(request, f'Terjadi kesalahan pada saat import File pada nomor BA {row["no_surat_bast"]}. Keterangan error : {e}')
                        return redirect(request.headers.get('Referer'))

                with transaction.atomic():
                    NoBAMetafisik.objects.bulk_create(obj_list)
                    valid_data = NoBAMetafisik.objects.filter(id__in=[obj.id for obj in obj_list])
                    df_valid = pd.DataFrame(valid_data.values())
                    transaction.set_rollback(True)
            except IntegrityError as e:
                messages.warning(request, f'Terjadi kesalahan pada saat import File. Keterangan error : {e}')
                return redirect(request.headers.get('Referer'))
            except Exception as e:
                messages.warning(request, f'Terjadi kesalahan pada saat import File. Keterangan error : {e}')
                return redirect(request.headers.get('Referer'))

            return render(request, 'metafisik/preview_no_ba_cbg_metafisik.html',
                          {'preview_data_valid': df_valid,
                           'total_data_valid': len(df_valid),
                           'file_name': file_name})

    if request.method == 'POST' and request.POST.get('action') == 'confirm':
        list_data_import = ['No Surat Bast', 'Tgl Bast', 'Tgl Pelayanan', 'Kdkrlayan', 'Kdkclayan', 'Kdppklayan',
                            'Nmppklayan', 'Total Klaim']
        file_name = request.POST.get('file_name')
        try:
            data_frame = pd.read_excel(storage.path(name=file_name), usecols=list_data_import)
            data_frame = data_frame.replace(np.nan, None)
            data_frame['Tgl Bast'] = pd.to_datetime(data_frame['Tgl Bast'])
            data_frame['Tgl Pelayanan'] = pd.to_datetime(data_frame['Tgl Pelayanan'])
            data_frame['Kdkclayan'] = data_frame['Kdkclayan'].astype('str').apply(lambda x: x.zfill(4))
            data_frame = data_frame.rename(columns={'No Surat Bast': 'no_surat_bast',
                                                    'Tgl Bast': 'tgl_bast',
                                                    'Tgl Pelayanan': 'tgl_pelayanan',
                                                    'Kdkrlayan': 'kdkrlayan',
                                                    'Kdkclayan': 'kdkclayan',
                                                    'Kdppklayan': 'kdppklayan',
                                                    'Nmppklayan': 'nmppklayan',
                                                    'Total Klaim': 'total_klaim',
                                                    })
        except Exception as e:
            messages.warning(request, f'Terjadi kesalahan pada saat import File. Keterangan error : {e}')
            return redirect(request.headers.get('Referer'))

        try:
            with transaction.atomic():
                NoBAMetafisik.objects.bulk_create(
                    [NoBAMetafisik(**dict(row[1])) for row in data_frame.iterrows()]
                )
            messages.success(request, 'Data List No BA CBG Metafisik berhasil dimport')
        except Exception as e:
            messages.error(request, f"Terjadi kesalahan: {e}")
            return redirect(request.headers.get('Referer'))

    context = {
        'import_form': import_form
    }

    return render(request, 'metafisik/import_no_ba_cbg_metafisik.html', context)

@login_required
@check_device
@permissions(role=['supervisorkp'])
def import_data_klaim_cbg_metafisik(request):
    storage = TemporaryStorage()
    import_form = ImportDataKlaimCBGMetafisikForm()
    list_data_import = ['No Surat Bast', 'Nokapst', 'Tgldtgsep', 'Tglplgsep', 'Nosjp', 'Nmtkp',
                        'Kdinacbgs', 'Nminacbgs', 'Kddiagprimer', 'Nmdiagprimer', 'Diagsekunder', 'Prosedur',
                        'Klsrawat', 'Nmjnspulang', 'politujsep', 'Kddokter', 'Nmdokter', 'Umur Tahun', 'Kdsa',
                        'Kdsd', 'Deskripsisd', 'Kdsi', 'Kdsp', 'Deskripsisp', 'Kdsr', 'Deskripsisr', 'Tarifsa',
                        'Tarifsd', 'Tarifsi', 'Tarifsp', 'Tarifsr', 'Bytagsep', 'Tarifgrup', 'biayars', 'id_logik', 'redflag',
                        'deskripsi_redflag', 'keterangan_aksi', 'indikator']
    if request.method == 'POST' and request.POST.get('action') == 'import':
        import_form = ImportDataKlaimCBGMetafisikForm(files=request.FILES, data=request.POST)
        if import_form.is_valid():
            file_name = f'{uuid.uuid4()}-{int(round(time.time() * 1000))}.xlsx'
            storage.save(name=file_name, content=import_form.cleaned_data.get('file'))
            try:
                data_frame = pd.read_excel(storage.path(name=file_name), usecols=list_data_import)
                data_frame = data_frame.replace(np.nan, '')
                # data_frame['Umur Tahun'] = data_frame['Umur Tahun'].str.replace(r'[^\d]', '', regex=True).astype(int)

                # Buat list kosong untuk menyimpan instance dari NoBAMetafisik
                no_ba_metafisik_instances = []

                # Iterasi setiap baris pada DataFrame
                for index, row in data_frame.iterrows():
                    try:
                        # Ambil instance NoBAMetafisik berdasarkan 'No Surat Bast'
                        no_ba_instance = NoBAMetafisik.objects.get(no_surat_bast=row['No Surat Bast'])

                        if no_ba_instance == '':
                            messages.warning(request, f'No Surat Bast {row["No Surat Bast"]} tidak ditemukan')
                            return redirect(request.headers.get('Referer'))

                        if no_ba_instance.is_import is True:
                            messages.warning(request, f'Data Klaim utuk No Surat Bast {row["No Surat Bast"]} sudah dilakukan upload')
                            return redirect(request.headers.get('Referer'))
                        # no_ba_instance.save()  # Simpan perubahan ke database

                        # Tambahkan instance ke list
                        no_ba_metafisik_instances.append(no_ba_instance)
                    except NoBAMetafisik.DoesNotExist:
                        messages.warning(request, f'No Surat Bast {row["No Surat Bast"]} tidak ditemukan di database List No BA Metafisik')
                        return redirect(request.headers.get('Referer'))

                # Assign instance ke kolom 'No Surat Bast' di DataFrame
                data_frame['No Surat Bast'] = no_ba_metafisik_instances

                # ubah nama colom
                data_frame = data_frame.rename(columns={'No Surat Bast': 'no_bast',
                                                        'Nokapst': 'nokapst',
                                                        'Tgldtgsep': 'tgldtgsep',
                                                        'Tglplgsep': 'tglplgsep',
                                                        'Nosjp': 'nosjp',
                                                        'Nmtkp': 'nmtkp',
                                                        'Kdinacbgs': 'kdinacbgs',
                                                        'Nminacbgs': 'nminacbgs',
                                                        'Kddiagprimer': 'kddiagprimer',
                                                        'Nmdiagprimer': 'nmdiagprimer',
                                                        'Diagsekunder': 'diagsekunder',
                                                        'Prosedur': 'prosedur',
                                                        'Klsrawat': 'klsrawat',
                                                        'Nmjnspulang': 'nmjnspulang',
                                                        'Kddokter': 'kddokter',
                                                        'Nmdokter': 'nmdokter',
                                                        'Umur Tahun': 'umur_tahun',
                                                        'Kdsa': 'kdsa',
                                                        'Kdsd': 'kdsd',
                                                        'Deskripsisd': 'deskripsisd',
                                                        'Kdsi': 'kdsi',
                                                        'Kdsp': 'kdsp',
                                                        'Deskripsisp': 'deskripsisp',
                                                        'Kdsr': 'kdsr',
                                                        'Deskripsisr': 'deskripsisr',
                                                        'Tarifsa': 'tarifsa',
                                                        'Tarifsd': 'tarifsd',
                                                        'Tarifsi': 'tarifsi',
                                                        'Tarifsp': 'tarifsp',
                                                        'Tarifsr': 'tarifsr',
                                                        'biayars': 'biayars',
                                                        'Bytagsep': 'bytagsep',
                                                        'Tarifgrup': 'tarifgrup',
                                                        })
            except Exception as e:
                messages.warning(request, f'Terjadi kesalahan pada saat import File. Keterangan error : {e}')
                return redirect(request.headers.get('Referer'))

            try:
                obj_list = []
                for _, row in data_frame.iterrows():
                    data_klaim = DataKlaimCBGMetafisik()
                    try:
                        data_klaim = DataKlaimCBGMetafisik(**dict(row))
                        data_klaim.full_clean()  # Validate the object
                        obj_list.append(data_klaim)
                    except Exception as e:
                        messages.warning(request, f'Terjadi kesalahan pada saat import File. Keterangan error : {e}')
                        return redirect(request.headers.get('Referer'))

                with transaction.atomic():
                    DataKlaimCBGMetafisik.objects.bulk_create(obj_list)
                    valid_data = DataKlaimCBGMetafisik.objects.filter(id__in=[obj.id for obj in obj_list])
                    df_valid = pd.DataFrame(valid_data.values())
                    transaction.set_rollback(True)
            except IntegrityError as e:
                messages.warning(request, f'Terjadi kesalahan pada saat import File. Keterangan error : {e}')
                return redirect(request.headers.get('Referer'))
            except Exception as e:
                messages.warning(request, f'Terjadi kesalahan pada saat import File. Keterangan error : {e}')
                return redirect(request.headers.get('Referer'))

            return render(request, 'metafisik/preview_data_klaim_cbg_metafisik.html',
                          {'preview_data_valid': df_valid,
                           'total_data_valid': len(df_valid),
                           'file_name': file_name})

    if request.method == 'POST' and request.POST.get('action') == 'confirm':
        file_name = request.POST.get('file_name')
        try:
            data_frame = pd.read_excel(storage.path(name=file_name), usecols=list_data_import)
            data_frame = data_frame.replace(np.nan, '')
            # data_frame['Umur Tahun'] = data_frame['Umur Tahun'].str.replace(r'[^\d]', '', regex=True).astype(int)

            # Buat list kosong untuk menyimpan instance dari NoBAMetafisik
            no_ba_metafisik_instances = []

            # Iterasi setiap baris pada DataFrame
            for index, row in data_frame.iterrows():
                try:
                    # Ambil instance NoBAMetafisik berdasarkan 'No Surat Bast'
                    no_ba_instance = NoBAMetafisik.objects.get(no_surat_bast=row['No Surat Bast'])

                    # Tambahkan instance ke list
                    no_ba_metafisik_instances.append(no_ba_instance)
                except NoBAMetafisik.DoesNotExist:
                    no_ba_metafisik_instances.append(None)  # Tambahkan None jika tidak ditemukan

            # Assign instance ke kolom 'No Surat Bast' di DataFrame
            data_frame['No Surat Bast'] = no_ba_metafisik_instances

            # ubah nama colom
            data_frame = data_frame.rename(columns={'No Surat Bast': 'no_bast',
                                                    'Nokapst': 'nokapst',
                                                    'Tgldtgsep': 'tgldtgsep',
                                                    'Tglplgsep': 'tglplgsep',
                                                    'Nosjp': 'nosjp',
                                                    'Nmtkp': 'nmtkp',
                                                    'Kdinacbgs': 'kdinacbgs',
                                                    'Nminacbgs': 'nminacbgs',
                                                    'Kddiagprimer': 'kddiagprimer',
                                                    'Nmdiagprimer': 'nmdiagprimer',
                                                    'Diagsekunder': 'diagsekunder',
                                                    'Prosedur': 'prosedur',
                                                    'Klsrawat': 'klsrawat',
                                                    'Nmjnspulang': 'nmjnspulang',
                                                    'Kddokter': 'kddokter',
                                                    'Nmdokter': 'nmdokter',
                                                    'Umur Tahun': 'umur_tahun',
                                                    'Kdsa': 'kdsa',
                                                    'Kdsd': 'kdsd',
                                                    'Deskripsisd': 'deskripsisd',
                                                    'Kdsi': 'kdsi',
                                                    'Kdsp': 'kdsp',
                                                    'Deskripsisp': 'deskripsisp',
                                                    'Kdsr': 'kdsr',
                                                    'Deskripsisr': 'deskripsisr',
                                                    'Tarifsa': 'tarifsa',
                                                    'Tarifsd': 'tarifsd',
                                                    'Tarifsi': 'tarifsi',
                                                    'Tarifsp': 'tarifsp',
                                                    'Tarifsr': 'tarifsr',
                                                    'biayars': 'biayars',
                                                    'Bytagsep': 'bytagsep',
                                                    'Tarifgrup': 'tarifgrup',
                                                    })
        except Exception as e:
            messages.warning(request, f'Terjadi kesalahan pada saat import File. Keterangan error : {e}')
            return redirect(request.headers.get('Referer'))

        try:
            with transaction.atomic():
                DataKlaimCBGMetafisik.objects.bulk_create(
                    [DataKlaimCBGMetafisik(**dict(row[1])) for row in data_frame.iterrows()]
                )

                # Ekstrak ID dari data_frame['no_bast']
                no_bast_ids = [bast.id for bast in data_frame['no_bast']]

                # Filter NoBAMetafisik sesuai dengan data_frame['no_bast']
                no_bast = NoBAMetafisik.objects.filter(id__in=no_bast_ids)

                # Bulk update untuk is_import=True dan total_redflag=0
                no_bast.update(is_import=True, total_redflag=0)

                # Annotate dengan redflag_count
                updated_bast = no_bast.annotate(redflag_count=Count('dataklaimcbgmetafisik'))

                # List untuk bulk_update
                update_list = []

                for bast in updated_bast:
                    bast.total_redflag = bast.redflag_count
                    update_list.append(bast)

                # Bulk update total_redflag berdasarkan hasil perhitungan redflag_count
                NoBAMetafisik.objects.bulk_update(update_list, ['total_redflag'])
            messages.success(request, 'Data Klaim CBG Metafisik berhasil dimport')
        except Exception as e:
            messages.warning(request, f"Terjadi kesalahan: {e}")
            return redirect(request.headers.get('Referer'))
    context = {
        'import_form': import_form,
    }
    return render(request, 'metafisik/import_data_klaim_cbg_metafisik.html', context)
