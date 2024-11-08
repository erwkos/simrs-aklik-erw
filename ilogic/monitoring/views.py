from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from klaim.models import DataKlaimCBG, DataKlaimObat
from user.decorators import permissions, check_device
from django.http import JsonResponse

from verifikator.models import HitungDataKlaim


@login_required
@check_device
@permissions(role=['verifikator'])
def api_json_data_klaim_CBG(request):
    # Get all KantorCabang associated with the user
    kantor_cabang_list = request.user.kantorcabang_set.all()

    # Build the queryset
    queryset = DataKlaimCBG.objects.select_related(
        'register_klaim', 'faskes', 'verifikator'
    ).filter(
        register_klaim__faskes__kantor_cabang__in=kantor_cabang_list,
        prosesklaim=False
    ).values(
        'register_klaim__nomor_register_klaim',
        'bupel',
        'faskes__nama',
        'verifikator__username',
        'status',
        'JNSPEL',
        'tgl_SLA'
    )

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
    # Get all KantorCabang associated with the user
    kantor_cabang_list = request.user.kantorcabang_set.all()

    # Build the queryset
    queryset = DataKlaimCBG.objects.select_related(
        'register_klaim', 'faskes', 'verifikator'
    ).filter(
        register_klaim__faskes__kantor_cabang__in=kantor_cabang_list,
        prosesklaim=False,
        verifikator=request.user
    ).values(
        'register_klaim__nomor_register_klaim',
        'bupel',
        'faskes__nama',
        'verifikator__username',
        'status',
        'JNSPEL',
        'tgl_SLA'
    )

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
    # Get all KantorCabang associated with the user
    kantor_cabang_list = request.user.kantorcabang_set.all()

    # Build the queryset
    queryset = DataKlaimCBG.objects.select_related(
        'register_klaim', 'faskes', 'verifikator'
    ).filter(
        register_klaim__faskes__kantor_cabang__in=kantor_cabang_list,
        prosesklaim=False
    ).values(
        'register_klaim__nomor_register_klaim',
        'bupel',
        'faskes__nama',
        'verifikator__username',
        'status',
        'JNSPEL',
        'tgl_SLA'
    )

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
    status_klaim = ('Pending', 'Dispute', 'Pembahasan', 'Tidak Layak')
    # Get all KantorCabang associated with the user
    kantor_cabang_list = request.user.kantorcabang_set.all()

    # Build the queryset
    queryset = DataKlaimCBG.objects.select_related(
        'register_klaim', 'faskes', 'verifikator'
    ).filter(
        register_klaim__faskes__kantor_cabang__in=kantor_cabang_list,
        prosesklaim=True,
        status__in=status_klaim,
    ).values(
        'register_klaim__nomor_register_klaim',
        'bupel',
        'faskes__nama',
        'verifikator__username',
        'status',
        'JNSPEL',
        'tgl_SLA'
    )

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
    # Get all KantorCabang associated with the user
    kantor_cabang_list = request.user.kantorcabang_set.all()

    # Build the queryset
    queryset = DataKlaimCBG.objects.select_related(
        'register_klaim', 'faskes', 'verifikator'
    ).filter(
        register_klaim__faskes__kantor_cabang__in=kantor_cabang_list,
        prosesklaim=False,
    ).values(
        'register_klaim__nomor_register_klaim',
        'bupel',
        'faskes__nama',
        'verifikator__username',
        'status',
        'JNSPEL',
        'tgl_SLA'
    )
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
    status_klaim = ('Pending', 'Dispute', 'Pembahasan', 'Tidak Layak')
    # Get all KantorCabang associated with the user
    kantor_cabang_list = request.user.kantorcabang_set.all()

    # Build the queryset
    queryset = DataKlaimCBG.objects.select_related(
        'register_klaim', 'faskes', 'verifikator'
    ).filter(
        register_klaim__faskes__kantor_cabang__in=kantor_cabang_list,
        prosesklaim=True,
        status__in=status_klaim,
    ).values(
        'register_klaim__nomor_register_klaim',
        'bupel',
        'faskes__nama',
        'verifikator__username',
        'status',
        'JNSPEL',
        'tgl_SLA'
    )
    data = list(queryset)
    return JsonResponse(data, safe=False)


@login_required
@check_device
@permissions(role=['adminAK'])
def monitoring_data_klaim_pending_dispute_CBG_stafak(request):
    context = {}
    return render(request, 'monitoring/monitoring_data_klaim_pending_dispute_CBG_stafak.html', context=context)


@login_required
@check_device
@permissions(role=['supervisor'])
def api_json_data_klaim_pending_dispute_CBG_supervisor(request):
    status_klaim = ('Pending', 'Dispute', 'Pembahasan', 'Tidak Layak')
    # Get all KantorCabang associated with the user
    kantor_cabang_list = request.user.kantorcabang_set.all()

    # Build the queryset
    queryset = DataKlaimCBG.objects.select_related(
        'register_klaim', 'faskes', 'verifikator'
    ).filter(
        register_klaim__faskes__kantor_cabang__in=kantor_cabang_list,
        prosesklaim=True,
        status__in=status_klaim,
    ).values(
        'register_klaim__nomor_register_klaim',
        'bupel',
        'faskes__nama',
        'verifikator__username',
        'status',
        'JNSPEL',
        'tgl_SLA'
    )
    data = list(queryset)
    return JsonResponse(data, safe=False)


@login_required
@check_device
@permissions(role=['supervisor'])
def monitoring_data_klaim_pending_dispute_CBG_supervisor(request):
    context = {}
    return render(request, 'monitoring/monitoring_data_klaim_pending_dispute_CBG_supervisor.html', context=context)


############################
# Obat #####################
############################


@login_required
@check_device
@permissions(role=['verifikator'])
def api_json_data_klaim_obat_verifikator(request):
    # Retrieve all KantorCabang associated with the user
    kantor_cabang_list = request.user.kantorcabang_set.all()

    # Build the queryset using related fields
    queryset = DataKlaimObat.objects.select_related('register_klaim', 'faskes', 'verifikator').filter(
        register_klaim__faskes__kantor_cabang__in=kantor_cabang_list,
        prosesklaim=False,
    ).values(
        'register_klaim__nomor_register_klaim',
        'bupel',
        'faskes__nama',
        'verifikator__username',
        'status',
        'KdJenis',
        'tgl_SLA'
    )

    data = list(queryset)
    return JsonResponse(data, safe=False)


@login_required
@check_device
@permissions(role=['verifikator'])
def monitoring_data_klaim_obat_verifikator(request):
    context = {}
    return render(request, 'monitoring/monitoring_data_klaim_obat_verifikator.html', context=context)


@login_required
@check_device
@permissions(role=['adminAK'])
def api_json_data_klaim_obat_stafak(request):
    # Retrieve all KantorCabang associated with the user
    kantor_cabang_list = request.user.kantorcabang_set.all()

    # Build the queryset using related fields
    queryset = DataKlaimObat.objects.select_related('register_klaim', 'faskes', 'verifikator').filter(
        register_klaim__faskes__kantor_cabang__in=kantor_cabang_list,
        prosesklaim=False,
    ).values(
        'register_klaim__nomor_register_klaim',
        'bupel',
        'faskes__nama',
        'verifikator__username',
        'status',
        'KdJenis',
        'tgl_SLA'
    )

    data = list(queryset)
    return JsonResponse(data, safe=False)

@login_required
@check_device
@permissions(role=['adminAK'])
def monitoring_data_klaim_obat_stafak(request):
    context = {}
    return render(request, 'monitoring/monitoring_data_klaim_obat_stafak.html', context=context)


@login_required
@check_device
@permissions(role=['supervisor'])
def api_json_data_klaim_obat_supervisor(request):
    # Retrieve all KantorCabang associated with the user
    kantor_cabang_list = request.user.kantorcabang_set.all()

    # Build the queryset using related fields
    queryset = DataKlaimObat.objects.select_related('register_klaim', 'faskes', 'verifikator').filter(
        register_klaim__faskes__kantor_cabang__in=kantor_cabang_list,
        prosesklaim=False,
    ).values(
        'register_klaim__nomor_register_klaim',
        'bupel',
        'faskes__nama',
        'verifikator__username',
        'status',
        'KdJenis',
        'tgl_SLA'
    )

    data = list(queryset)
    return JsonResponse(data, safe=False)


@login_required
@check_device
@permissions(role=['supervisor'])
def monitoring_data_klaim_obat_supervisor(request):
    context = {}
    return render(request, 'monitoring/monitoring_data_klaim_obat_supervisor.html', context=context)




@login_required
@check_device
@permissions(role=['verifikator'])
def api_json_data_klaim_pending_dispute_obat_verifikator(request):
    status_klaim = ('Pending', 'Dispute', 'Pembahasan', 'Tidak Layak')
    # Retrieve all KantorCabang associated with the user
    kantor_cabang_list = request.user.kantorcabang_set.all()

    # Build the queryset using related fields
    queryset = DataKlaimObat.objects.select_related('register_klaim', 'faskes', 'verifikator').filter(
        register_klaim__faskes__kantor_cabang__in=kantor_cabang_list,
        prosesklaim=True,
        status__in=status_klaim
    ).values(
        'register_klaim__nomor_register_klaim',
        'bupel',
        'faskes__nama',
        'verifikator__username',
        'status',
        'KdJenis',
        'tgl_SLA'
    )

    data = list(queryset)
    return JsonResponse(data, safe=False)


@login_required
@check_device
@permissions(role=['verifikator'])
def monitoring_data_klaim_pending_dispute_obat_verifikator(request):
    context = {}
    return render(request, 'monitoring/monitoring_data_klaim_pending_dispute_obat_verifikator.html', context=context)


@login_required
@check_device
@permissions(role=['adminAK'])
def api_json_data_klaim_pending_dispute_obat_stafak(request):
    status_klaim = ('Pending', 'Dispute', 'Pembahasan', 'Tidak Layak')
    # Retrieve all KantorCabang associated with the user
    kantor_cabang_list = request.user.kantorcabang_set.all()

    # Build the queryset using related fields
    queryset = DataKlaimObat.objects.select_related('register_klaim', 'faskes', 'verifikator').filter(
        register_klaim__faskes__kantor_cabang__in=kantor_cabang_list,
        prosesklaim=True,
        status__in=status_klaim
    ).values(
        'register_klaim__nomor_register_klaim',
        'bupel',
        'faskes__nama',
        'verifikator__username',
        'status',
        'KdJenis',
        'tgl_SLA'
    )

    data = list(queryset)
    return JsonResponse(data, safe=False)



@login_required
@check_device
@permissions(role=['adminAK'])
def monitoring_data_klaim_pending_dispute_obat_stafak(request):
    context = {}
    return render(request, 'monitoring/monitoring_data_klaim_pending_dispute_obat_stafak.html', context=context)


@login_required
@check_device
@permissions(role=['supervisor'])
def api_json_data_klaim_pending_dispute_obat_supervisor(request):
    status_klaim = ('Pending', 'Dispute', 'Pembahasan', 'Tidak Layak')
    # Retrieve all KantorCabang associated with the user
    kantor_cabang_list = request.user.kantorcabang_set.all()

    # Build the queryset using related fields
    queryset = DataKlaimObat.objects.select_related('register_klaim', 'faskes', 'verifikator').filter(
        register_klaim__faskes__kantor_cabang__in=kantor_cabang_list,
        prosesklaim=True,
        status__in=status_klaim
    ).values(
        'register_klaim__nomor_register_klaim',
        'bupel',
        'faskes__nama',
        'verifikator__username',
        'status',
        'KdJenis',
        'tgl_SLA'
    )

    data = list(queryset)
    return JsonResponse(data, safe=False)


@login_required
@check_device
@permissions(role=['supervisor'])
def monitoring_data_klaim_pending_dispute_obat_supervisor(request):
    context = {}
    return render(request, 'monitoring/monitoring_data_klaim_pending_dispute_obat_supervisor.html', context=context)
