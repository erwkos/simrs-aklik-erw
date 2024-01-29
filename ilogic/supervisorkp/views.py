from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from klaim.models import RegisterKlaim
from user.decorators import check_device, permissions


@login_required
@check_device
@permissions(role=['supervisorkp'])
def api_json_register_supervisorkp(request):
    queryset = RegisterKlaim.objects.all().values('faskes__nama', 'faskes__kantor_cabang__nama', 'bulan_pelayanan')
    data = list(queryset)
    return JsonResponse(data, safe=False)


@login_required
@check_device
@permissions(role=['supervisorkp'])
def monitoring_register_supervisorkp(request):
    context = {}
    return render(request, 'supervisorkp/monitoring_register_supervisorkp.html', context=context)
