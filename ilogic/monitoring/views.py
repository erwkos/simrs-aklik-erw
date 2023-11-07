from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from klaim.models import DataKlaimCBG
from user.decorators import permissions, check_device
from django.http import JsonResponse

from verifikator.models import HitungDataKlaim


@login_required
@check_device
@permissions(role=['verifikator'])
def api_json_data_klaim_CBG(request):
    queryset = DataKlaimCBG.objects.filter(register_klaim__nomor_register_klaim__startswith=
                                           request.user.kantorcabang_set.all().first().kode_cabang, prosesklaim=False).\
        values('register_klaim__nomor_register_klaim', 'bupel', 'faskes__nama', 'verifikator__username', 'status', 'JNSPEL',
               'tgl_SLA')
    data = list(queryset)
    return JsonResponse(data, safe=False)


@login_required
@check_device
@permissions(role=['verifikator'])
def monitoring_data_klaim_CBG(request):
    context = {}
    return render(request, 'monitoring/monitoring_data_klaim_CBG.html', context=context)


@login_required
@check_device
@permissions(role=['verifikator'])
def api_json_data_klaim_CBG_verifikator(request):
    queryset = DataKlaimCBG.objects.filter(register_klaim__nomor_register_klaim__startswith=
                                           request.user.kantorcabang_set.all().first().kode_cabang, prosesklaim=False,
                                           verifikator=request.user).\
        values('register_klaim__nomor_register_klaim', 'bupel', 'faskes__nama', 'verifikator__username', 'status', 'JNSPEL',
               'tgl_SLA')
    data = list(queryset)
    return JsonResponse(data, safe=False)


@login_required
@check_device
@permissions(role=['verifikator'])
def monitoring_data_klaim_CBG_verifikator(request):
    context = {}
    return render(request, 'monitoring/monitoring_data_klaim_CBG_verifikator.html', context=context)\



@login_required
@check_device
@permissions(role=['supervisor'])
def api_json_data_klaim_CBG_supervisor(request):
    queryset = DataKlaimCBG.objects.filter(register_klaim__nomor_register_klaim__startswith=
                                           request.user.kantorcabang_set.all().first().kode_cabang, prosesklaim=False).\
        values('register_klaim__nomor_register_klaim', 'bupel', 'faskes__nama', 'verifikator__username', 'status', 'JNSPEL',
               'tgl_SLA')
    data = list(queryset)
    return JsonResponse(data, safe=False)


@login_required
@check_device
@permissions(role=['supervisor'])
def monitoring_data_klaim_CBG_supervisor(request):
    context = {}
    return render(request, 'monitoring/monitoring_data_klaim_CBG_supervisor.html', context=context)


@login_required
@check_device
@permissions(role=['verifikator'])
def api_json_data_klaim_hitung_verifikator(request):
    queryset = HitungDataKlaim.objects.filter(nomor_register_klaim__startswith=request.user.kantorcabang_set.all().first().kode_cabang,
                                              verifikator=request.user).\
        values('tglhitung', 'periodehitung', 'jenis_klaim', 'verifikator__username')
    data = list(queryset)
    return JsonResponse(data, safe=False)


@login_required
@check_device
@permissions(role=['verifikator'])
def monitoring_data_klaim_hitung_verifikator(request):
    context = {}
    return render(request, 'monitoring/monitoring_data_klaim_hitung_verifikator.html', context=context)


@login_required
@check_device
@permissions(role=['supervisor'])
def api_json_data_klaim_hitung_supervisor(request):
    queryset = HitungDataKlaim.objects.filter(nomor_register_klaim__startswith=request.user.kantorcabang_set.all().first().kode_cabang,).\
        values('tglhitung', 'periodehitung', 'jenis_klaim', 'verifikator__username')
    data = list(queryset)
    return JsonResponse(data, safe=False)


@login_required
@check_device
@permissions(role=['supervisor'])
def monitoring_data_klaim_hitung_supervisor(request):
    context = {}
    return render(request, 'monitoring/monitoring_data_klaim_hitung_supervisor.html', context=context)


@login_required
@check_device
@permissions(role=['verifikator'])
def api_json_data_klaim_pending_dispute_CBG(request):
    status_klaim = ('Pending', 'Dispute', 'Pembahasan')
    queryset = DataKlaimCBG.objects.filter(register_klaim__nomor_register_klaim__startswith=
                                           request.user.kantorcabang_set.all().first().kode_cabang,
                                           prosesklaim=True,
                                           status__in=status_klaim).\
        values('register_klaim__nomor_register_klaim', 'bupel', 'faskes__nama', 'verifikator__username', 'status', 'JNSPEL',
               'tgl_SLA')
    data = list(queryset)
    return JsonResponse(data, safe=False)


@login_required
@check_device
@permissions(role=['verifikator'])
def monitoring_data_klaim_pending_dispute_CBG(request):
    context = {}
    return render(request, 'monitoring/monitoring_data_klaim_pending_dispute_CBG.html', context=context)


@login_required
@check_device
@permissions(role=['adminAK'])
def api_json_data_klaim_CBG_stafak(request):
    queryset = DataKlaimCBG.objects.filter(register_klaim__nomor_register_klaim__startswith=
                                           request.user.kantorcabang_set.all().first().kode_cabang, prosesklaim=False).\
        values('register_klaim__nomor_register_klaim', 'bupel', 'faskes__nama', 'verifikator__username', 'status', 'JNSPEL',
               'tgl_SLA')
    data = list(queryset)
    return JsonResponse(data, safe=False)


@login_required
@check_device
@permissions(role=['adminAK'])
def monitoring_data_klaim_CBG_stafak(request):
    context = {}
    return render(request, 'monitoring/monitoring_data_klaim_CBG_stafak.html', context=context)


@login_required
@check_device
@permissions(role=['adminAK'])
def api_json_data_klaim_pending_dispute_CBG_stafak(request):
    status_klaim = ('Pending', 'Dispute', 'Pembahasan')
    queryset = DataKlaimCBG.objects.filter(register_klaim__nomor_register_klaim__startswith=
                                           request.user.kantorcabang_set.all().first().kode_cabang,
                                           prosesklaim=True,
                                           status__in=status_klaim).\
        values('register_klaim__nomor_register_klaim', 'bupel', 'faskes__nama', 'verifikator__username', 'status', 'JNSPEL',
               'tgl_SLA')
    data = list(queryset)
    return JsonResponse(data, safe=False)


@login_required
@check_device
@permissions(role=['adminAK'])
def monitoring_data_klaim_pending_dispute_CBG_stafak(request):
    context = {}
    return render(request, 'monitoring/monitoring_data_klaim_pending_dispute_CBG_stafak.html', context=context)