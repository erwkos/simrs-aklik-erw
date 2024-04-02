from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from faskes.models import KantorCabang
from klaim.choices import StatusRegisterChoices
from klaim.filters import RegisterKlaimFaskesFilter
from .filters import DataKlaimAmbilNoSepFilter
from .forms import (
    StatusRegisterKlaimForm,
    PilihVerifikatorRegisterKlaimForm, AlasanDikembalikanForm, IsActiveForm, ProsesBOAForm
)
from klaim.models import (
    RegisterKlaim, DataKlaimCBG,
)
from user.decorators import permissions, check_device
from user.models import User
from datetime import timedelta


@login_required
@check_device
@permissions(role=['adminAK'])
def daftar_register_klaim(request):
    queryset = RegisterKlaim.objects.filter(
        nomor_register_klaim__startswith=request.user.kantorcabang_set.all().first().kode_cabang).order_by('-tgl_aju')

    # filter
    myFilter = RegisterKlaimFaskesFilter(request.GET, queryset=queryset, request=request)
    queryset = myFilter.qs

    # pagination
    paginator = Paginator(queryset, 25)
    page_number = request.GET.get('page')
    queryset = paginator.get_page(page_number)

    context = {
        'register_list': queryset,
        'myFilter': myFilter,
    }

    return render(request, 'staff/daftar_register.html', context)


@login_required
@check_device
@permissions(role=['adminAK'])
def detail_register(request, pk):
    kantor_cabang = request.user.kantorcabang_set.all().first()
    queryset = RegisterKlaim.objects.filter(
        nomor_register_klaim__startswith=kantor_cabang.kode_cabang)
    instance = queryset.get(id=pk)
    status_form = StatusRegisterKlaimForm(instance=instance)
    # pilih_verifikator_form = PilihVerifikatorRegisterKlaimForm(instance=instance)

    # hanya bisa dibagi PIC nya hanya untuk verifikator yg aktif dan statusnya staf
    status_form.fields['verifikator'].queryset = kantor_cabang.user.filter(
        groups__in=Group.objects.filter(name='verifikator'), is_active=True, is_staff=True)
    # # hanya bisa dibagi PIC nya hanya untuk verifikator yg aktif dan statusnya staf
    # pilih_verifikator_form.fields['verifikator'].queryset = kantor_cabang.user.filter(
    #     groups__in=Group.objects.filter(name='verifikator'), is_active=True, is_staff=True)

    # alasan_dikembalikan_form = AlasanDikembalikanForm(instance=instance)
    if request.method == 'POST' and request.POST.get('action') == 'update_status':
        status_form = StatusRegisterKlaimForm(instance=instance, data=request.POST)
        if status_form.is_valid():
            status_form.save()
            # dari model dipindah ke sini untuk pembuatan tgl ba lengkap
            # instance.tgl_ba_lengkap = instance.tgl_terima + timedelta(days=9)
            # instance.save()
            if instance.status == 'Terima':
                messages.warning(request, "Klaim berhasil diterima. Selanjutnya dapat memberikan informasi "
                                          "ke PIC Klaim. Terima Kasih")
            elif instance.status == 'Dikembalikan':
                instance.tgl_terima = None
                instance.tgl_ba_lengkap = None
                instance.no_ba_terima = None
                instance.verifikator = None
                instance.save()
                messages.info(request, "Klaim berhasil dikembalikan. "
                                       "Selanjutnya dapat memberikan informasi ke fasilitas kesehatan. Terima Kasih")
            return redirect(request.headers.get('Referer'))
        else:
            messages.warning(request, "Proses Simpan Register Klaim Gagal")
            return redirect(request.headers.get('Referer'))
    # if request.method == 'POST' and request.POST.get('action') == 'pilih_verifikator':
    #     pilih_verifikator_form = PilihVerifikatorRegisterKlaimForm(instance=instance, data=request.POST)
    #     if pilih_verifikator_form.is_valid():
    #         pilih_verifikator_form.save()
    #         messages.success(request, "Pilih PIC Berhasil. Selanjutnya dapat memberikan informasi ke Verifikator. "
    #                                   "Terima Kasih")
    #         return redirect(request.headers.get('Referer'))
    #     else:
    #         messages.warning(request, "Proses Simpan Register Klaim Gagal")
    #         return redirect(request.headers.get('Referer'))
    #
    # if request.method == 'POST' and request.POST.get('action') == 'alasan_dikembalikan':
    #     alasan_dikembalikan_form = AlasanDikembalikanForm(instance=instance, data=request.POST)
    #     if alasan_dikembalikan_form.is_valid():
    #         alasan_dikembalikan_form.save()
    #         messages.success(request, "Keterangan Pengembalian berhasil disimpan. Terima Kasih")
    #         return redirect(request.headers.get('Referer'))
    #     else:
    #         messages.warning(request, "Proses Simpan Register Klaim Gagal")
    #         return redirect(request.headers.get('Referer'))
    context = {
        'register': instance,
        'status_form': status_form,
        # 'pilih_verifikator_form': pilih_verifikator_form,
        # 'alasan_dikembalikan_form': alasan_dikembalikan_form,
    }
    return render(request, 'staff/detail_register.html', context)

# def monitoring_data_klaim(request):
#     kantor_cabang = request.user.kantorcabang_set.first()
#     verifikator_list = User.objects.filter(groups__name='verifikator')
#     context = {
#         'verifikator_list': verifikator_list
#     }
#     return render(request, 'staff/monitoring_data_klaim.html', context)


@login_required
@check_device
@permissions(role=['adminAK'])
def list_user_verifikator(request):
    verifikator_group = Group.objects.filter(name='verifikator').first()
    user_verifikator = (User.objects.filter(groups=verifikator_group,
                                            kantorcabang__in=request.user.kantorcabang_set.all()).
                        order_by('-is_staff'))

    content = {
        'verifikator': user_verifikator,
    }
    return render(request, 'staff/list_user_verifikator.html', content)


@login_required
@check_device
@permissions(role=['adminAK'])
def edit_user_verifikator(request, pk):
    queryset = User.objects.filter(kantorcabang=request.user.kantorcabang_set.all().first())
    instance = queryset.get(id=pk)
    # user = User.objects.get(pk=pk)
    form = IsActiveForm(instance=instance)
    if request.method == 'POST':
        form = IsActiveForm(data=request.POST, instance=instance)
        if not form.has_changed():
            messages.warning(request, f'Status {instance} tidak ada perubahan')
            return redirect('staff:list_user_verifikator')
        elif form.is_valid():
            form.save()
            messages.success(request, f'Status {instance} berhasil diubah')
            return redirect('staff:list_user_verifikator')
        else:
            form = IsActiveForm()
            messages.warning(request, f'Status {instance} tidak berhasil diubah')

    content = {
        'form': form,
        'instance': instance
    }
    return render(request, 'staff/edit_user_verifikator.html', content)


@login_required
@check_device
@permissions(role=['adminAK'])
def ambil_nosep_cbg(request):
    register_klaim = request.GET.get('nomor_register_klaim')
    queryset = DataKlaimCBG.objects.filter(faskes__kantor_cabang=request.user.kantorcabang_set.all().first(),
                                           prosesklaim=False, register_klaim__nomor_register_klaim=register_klaim)
    data = queryset.first()
    myFilter = DataKlaimAmbilNoSepFilter(request.GET, queryset=queryset)
    queryset = myFilter.qs

    list_nosep = []
    for file in queryset:
        list_nosep.append(file.NOSEP)

    nosep = "|".join(list_nosep)

    context = {
        'data': data,
        'myFilter': myFilter,
        'nosep': nosep,
    }

    return render(request, 'staff/ambil_nosep_cbg.html', context)


@login_required
@check_device
@permissions(role=['adminAK'])
def daftar_proses_boa(request):
    queryset = RegisterKlaim.objects.filter(
        nomor_register_klaim__startswith=request.user.kantorcabang_set.all().first().kode_cabang,
        status=StatusRegisterChoices.SELESAI, prosesboa=False).order_by('-tgl_aju')

    # filter
    myFilter = RegisterKlaimFaskesFilter(request.GET, queryset=queryset, request=request)
    queryset = myFilter.qs

    # pagination
    paginator = Paginator(queryset, 25)
    page_number = request.GET.get('page')
    queryset = paginator.get_page(page_number)

    context = {
        'register_list': queryset,
        'myFilter': myFilter,
    }

    return render(request, 'staff/daftar_proses_boa.html', context)


@login_required
@check_device
@permissions(role=['adminAK'])
def edit_proses_boa(request, pk):
    kantor_cabang = request.user.kantorcabang_set.all().first()
    queryset = RegisterKlaim.objects.filter(
        nomor_register_klaim__startswith=kantor_cabang.kode_cabang, status=StatusRegisterChoices.SELESAI,
        prosesboa=False)
    instance = queryset.get(id=pk)
    form = ProsesBOAForm(instance=instance)
    if request.method == 'POST':
        form = ProsesBOAForm(data=request.POST, instance=instance)
        if form.is_valid():
            form.save()
            instance.prosesboa = True
            instance.save()
            messages.success(request, f'Register {instance} berhasil diupdate proses BOA')
            return redirect('staff:daftar_proses_boa')
        else:
            messages.warning(request, f'Register {instance} tidak berhasil diupdate proses BOA')
            return redirect(request.headers.get('Referer'))

    context = {
        'form': form,
        'register': instance,
    }
    return render(request, 'staff/edit_proses_boa.html', context)