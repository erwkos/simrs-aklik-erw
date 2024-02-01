from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, AdminPasswordChangeForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from faskes.models import KantorCabang
from klaim.models import RegisterKlaim
from supervisorkp.filters import UserSupervisorkpFilter
from supervisorkp.forms import EditUserSupervisorkpForm, CreateUserSupervisorkpForm
from user.decorators import check_device, permissions
from user.models import User


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


@login_required
@check_device
@permissions(role=['supervisorkp'])
def daftar_user_supervisorkp(request):
    queryset = User.objects.all().order_by('-date_joined')

    # filter
    myFilter = UserSupervisorkpFilter(request.GET, queryset=queryset)
    queryset = myFilter.qs

    # pagination
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    queryset = paginator.get_page(page_number)

    context = {
        'register_list': queryset,
        'myFilter': myFilter,
    }
    return render(request, 'supervisorkp/daftar_user_supervisorkp.html', context=context)


@login_required
@check_device
@permissions(role=['supervisorkp'])
def update_user_supervisorkp(request, pk):
    instance = get_object_or_404(User, pk=pk)
    form = EditUserSupervisorkpForm(instance=instance)
    if request.method == 'POST':
        form = EditUserSupervisorkpForm(data=request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data user berhasil diubah')
            return redirect('supervisorkp:daftar_user_supervisorkp')
        else:
            form = EditUserSupervisorkpForm()
            messages.warning(request, 'Data user tidak berhasil diubah')
    context = {'form': form,
               'instance': instance
               }
    return render(request, 'supervisorkp/update_user_supervisorkp.html', context=context)


@login_required
@check_device
@permissions(role=['supervisorkp'])
def add_user_supervisorkp(request):
    kc = KantorCabang.objects.all()
    if request.method == 'POST':
        form = CreateUserSupervisorkpForm(data=request.POST)
        if form.is_valid():
            add_kc = kc.filter(nama=request.POST.get('kc')).first()
            if add_kc is not None:
                try:
                    fm = form.save()
                    add_kc.user.add(fm)
                    messages.success(request, 'Data user berhasil ditambahkan')
                except Exception as e:
                    messages.warning(request, 'Terdapat error pada saat penambahan user :', str(e))
            elif add_kc is None:
                try:
                    form.save()
                    messages.success(request, 'Data user berhasil ditambahkan')
                except Exception as e:
                    messages.warning(request, 'Terdapat error pada saat penambahan user :', str(e))
        else:
            form = CreateUserSupervisorkpForm()
            messages.warning(request, 'Data user tidak berhasil ditambahkan')
    else:
        form = CreateUserSupervisorkpForm()
    context = {'form': form,
               'kc': kc}
    return render(request, 'supervisorkp/add_user_supervisorkp.html', context=context)


@login_required
@check_device
@permissions(role=['supervisorkp'])
def reset_password_supervisorkp(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = AdminPasswordChangeForm(user)
    if request.method == 'POST':
        form = AdminPasswordChangeForm(user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reset password berhasil')
            return redirect('supervisorkp:daftar_user_supervisorkp')
        else:
            form = AdminPasswordChangeForm(user)
            messages.warning(request, 'Reset password tidak berhasil')
    context = {'form': form,
               'instance': user
               }
    return render(request, 'supervisorkp/reset_password_supervisorkp.html', context=context)


