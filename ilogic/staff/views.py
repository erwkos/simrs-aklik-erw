from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from faskes.models import KantorCabang
from klaim.filters import RegisterKlaimFaskesFilter
from .forms import (
    StatusRegisterKlaimForm,
    PilihVerifikatorRegisterKlaimForm, AlasanDikembalikanForm, IsActiveForm
)
from klaim.models import (
    RegisterKlaim,
)
from user.decorators import permissions, check_device
from user.models import User


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
    pilih_verifikator_form = PilihVerifikatorRegisterKlaimForm(instance=instance)

    # hanya bisa dibagi PIC nya hanya untuk verifikator yg aktif dan statusnya staf
    pilih_verifikator_form.fields['verifikator'].queryset = kantor_cabang.user.filter(
        groups__in=Group.objects.filter(name='verifikator'), is_active=True, is_staff=True)

    alasan_dikembalikan_form = AlasanDikembalikanForm(instance=instance)
    if request.method == 'POST' and request.POST.get('action') == 'update_status':
        status_form = StatusRegisterKlaimForm(instance=instance, data=request.POST)
        if status_form.is_valid():
            status_form.save()
            if instance.status == 'Diterima':
                messages.warning(request, "Klaim berhasil diterima. Selanjutnya mohon isi Tgl Terima, No BA Terima, "
                                          "dan Pilih PIC Klaim. Terima Kasih")
            elif instance.status == 'Dikembalikan':
                messages.info(request, "Klaim berhasil dikembalikan. Selanjutnya isi alasan pengembalian. Terima Kasih")
            return redirect(request.headers.get('Referer'))
        else:
            messages.warning(request, "Proses Simpan Register Klaim Gagal")
            return redirect(request.headers.get('Referer'))
    if request.method == 'POST' and request.POST.get('action') == 'pilih_verifikator':
        pilih_verifikator_form = PilihVerifikatorRegisterKlaimForm(instance=instance, data=request.POST)
        if pilih_verifikator_form.is_valid():
            pilih_verifikator_form.save()
            messages.success(request, "Pilih PIC Berhasil. Selanjutnya dapat memberikan informasi ke Verifikator. "
                                      "Terima Kasih")
            return redirect(request.headers.get('Referer'))
        else:
            messages.warning(request, "Proses Simpan Register Klaim Gagal")
            return redirect(request.headers.get('Referer'))

    if request.method == 'POST' and request.POST.get('action') == 'alasan_dikembalikan':
        alasan_dikembalikan_form = AlasanDikembalikanForm(instance=instance, data=request.POST)
        if alasan_dikembalikan_form.is_valid():
            alasan_dikembalikan_form.save()
            messages.success(request, "Keterangan Pengembalian berhasil disimpan. Terima Kasih")
            return redirect(request.headers.get('Referer'))
        else:
            messages.warning(request, "Proses Simpan Register Klaim Gagal")
            return redirect(request.headers.get('Referer'))
    context = {
        'register': instance,
        'status_form': status_form,
        'pilih_verifikator_form': pilih_verifikator_form,
        'alasan_dikembalikan_form': alasan_dikembalikan_form,
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
                        order_by('is_active'))

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
        if form.is_valid():
            form.save()
            messages.success(request, 'Status berhasil diubah')
            return redirect('staff:list_user_verifikator')
        else:
            form = IsActiveForm()
            messages.warning(request, 'Status tidak berhasil diubah')

    content = {
        'form': form,
    }
    return render(request, 'staff/edit_user_verifikator.html', content)