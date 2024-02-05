import traceback

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone

from dokumentasi.forms import PolaRulesForm
from dokumentasi.models import PolaRules, ProgressVersion
from user.decorators import check_device, permissions

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from user.models import User
from .models import PolaRules
from .serializers import PolaRulesSerializer
from rest_framework import viewsets


class PolaRulesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PolaRules.objects.all()
    serializer_class = PolaRulesSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


@login_required
@check_device
@permissions(role=['entrilogik'])
def list_pola_rules(request):
    progressversion = ProgressVersion.objects.all().last()
    queryset = PolaRules.objects.filter(progress_version__version=progressversion.version)
    version_selected = progressversion.version
    user_saya = User.objects.get(id=request.user.id)
    saya_entrilogik = False
    saya_asdep = False
    saya_depdirbid = False
    for x in user_saya.groups.all():
        if str(x) == 'entrilogik':
            saya_entrilogik = True
        if str(x) == 'asdep':
            saya_asdep = True
        if str(x) == 'depdirbid':
            saya_depdirbid = True
    context = {
        'queryset': queryset,
        'version_selected': version_selected,
        'progressversion': progressversion,
        'saya_entrilogik': saya_entrilogik,
        'saya_asdep': saya_asdep,
        'saya_depdirbid': saya_depdirbid
    }
    return render(request, 'dokumentasi/list_pola_rules.html', context)


@login_required
@check_device
@permissions(role=['entrilogik'])
def edit_pola_rules(request, pk):
    try:
        queryset = PolaRules.objects.all()
        polarules = PolaRules.objects.get(id=pk)
        if request.method == 'POST':
            data = request.POST
            los_data = None
            if data.get('los') == '':
                pass
            else:
                los_data = data.get('los')
            usia_data = None
            if data.get('usia') == '':
                pass
            else:
                usia_data = data.get('usia')
            polarules.nama_rules = data.get('nama_rules')
            polarules.diagnosis_utama = data.get('diagnosis_utama_combined')
            polarules.diagnosis_sekunder = data.get('diagnosis_sekunder_combined')
            polarules.prosedur = data.get('prosedur_combined')
            polarules.jenis_pelayanan = data.get('jenis_pelayanan')
            polarules.cmg = data.get('cmg')
            polarules.los = los_data
            polarules.cbg = data.get('cbg')
            polarules.jenis_kelamin = data.get('jenis_kelamin')
            polarules.severity_level = data.get('severity_level')
            polarules.usia = usia_data
            polarules.pesan = data.get('pesan')
            polarules.models_polarules = data.get('models_polarules')
            polarules.save()
            messages.info(request, 'Telah Diubah Pola Rules : {0}'.format(polarules.nama_rules))
            return redirect('/dokumentasi/list/pola-rules')
        context = {
            'queryset': queryset,
            'polarules': polarules,
        }
        return render(request, 'dokumentasi/edit_pola_rules.html', context)
    except Exception as e:
        messages.info(request, '{0}'.format(e))
        return redirect('/dokumentasi/list/pola-rules')


@login_required
@check_device
@permissions(role=['entrilogik'])
def add_pola_rules(request):
    queryset = PolaRules.objects.all()
    progressversion = ProgressVersion.objects.all().last()
    version_selected = progressversion.version
    if progressversion.is_aju is True and progressversion.is_approved_asdep is False:
        messages.warning(request, 'Anda Belum Bisa Menambahkan Logic Karena Masih Dalam Tahapan Pengajuan ke Asdep')
    if progressversion.is_aju is True and progressversion.is_approved_asdep is True and progressversion.is_approved_depdirbid is False:
        messages.warning(request, 'Anda Belum Bisa Menambahkan Logic Karena Masih Dalam Tahapan Approval Depdirbid')
        return redirect('/dokumentasi/list/pola-rules')
    if progressversion.is_aju is True and progressversion.is_approved_asdep is True and progressversion.is_approved_depdirbid is True:
        version_selected = progressversion.version + 1
    if request.method == 'POST':
        data = request.POST
        if progressversion is None:
            progressversion = ProgressVersion(
                version=version_selected
            )
            progressversion.save()
        elif progressversion.is_aju is True and progressversion.is_approved_asdep is True and progressversion.is_approved_depdirbid is True:
            version_selected = progressversion.version + 1
            progressversion = ProgressVersion(
                version=version_selected
            )
            progressversion.save()
        los_data = None
        if data.get('los') == '':
            pass
        else:
            los_data = data.get('los')
        usia_data = None
        if data.get('usia') == '':
            pass
        else:
            usia_data = data.get('usia')
        polarules = PolaRules(
            progress_version=progressversion,
            nama_rules=data.get('nama_rules'),
            diagnosis_utama=data.get('diagnosis_utama_combined'),
            diagnosis_sekunder=data.get('diagnosis_sekunder_combined'),
            prosedur=data.get('prosedur_combined'),
            jenis_pelayanan=data.get('jenis_pelayanan'),
            cmg=data.get('cmg'),
            los=los_data,
            cbg=data.get('cbg'),
            severity_level=data.get('severity_level'),
            jenis_kelamin=data.get('jenis_kelamin'),
            usia=usia_data,
            pesan=data.get('pesan'),
            models_polarules=data.get('models_polarules')
        )
        polarules.save()
        messages.info(request, 'Data Pola Rules Entry Logic Sudah Ditambahkan')
        return redirect('/dokumentasi/list/pola-rules')
    context = {
        'queryset': queryset,
        'version_selected': version_selected,
    }
    return render(request, 'dokumentasi/add_pola_rules.html', context)


@login_required
@check_device
@permissions(role=['entrilogik'])
def delete_pola_rules(request, pk):
    if request.method == 'POST':
        queryset = PolaRules.objects.all()
        instance = queryset.get(id=pk)
        instance.delete()
        messages.info(request, 'Telah Dihapus Pola Rules : {0}'.format(instance.nama_rules))
        return redirect('/dokumentasi/list/pola-rules')
    else:
        messages.info(request, 'Anda tidak dapat menghapus dengan metode ini')
        return redirect('/dokumentasi/list/pola-rules')


@login_required
@check_device
@permissions(role=['entrilogik'])
def ajukan_pola_rules(request, pk):
    if request.method == 'POST':
        queryset = ProgressVersion.objects.all()
        instance = queryset.get(pk=pk)
        instance.is_aju = True
        instance.dt_is_aju = timezone.now()
        instance.is_approved_asdep = False
        instance.dt_is_approved_asdep = timezone.now()
        instance.is_approved_depdirbid = False
        instance.dt_is_approved_depdirbid = timezone.now()
        instance.open_edit = False
        instance.save()
        messages.info(request, 'Telah Diajukan Versi Pola Rules : 1.{0}'.format(instance.version))
        return redirect('/dokumentasi/list/pola-rules')
    else:
        messages.info(request, 'Anda Tidak Dapat Melakukan Pengajuan Dengan Metode Ini')
        return redirect('/dokumentasi/list/pola-rules')


@login_required
@check_device
@permissions(role=['asdep'])
def approved_asdep_pola_rules(request, pk):
    queryset = ProgressVersion.objects.all()
    instance = queryset.get(pk=pk)
    if request.method == 'POST' and instance.is_aju is True and instance.is_approved_asdep is False:
        instance.is_approved_asdep = True
        instance.dt_is_approved_asdep = timezone.now()
        instance.open_edit = False
        instance.save()
        messages.info(request, 'Telah Disetujui oleh Asdep Versi Pola Rules : 1.{0}'.format(instance.version))
        return redirect('/dokumentasi/list/pola-rules')
    else:
        messages.info(request, 'Anda Tidak Dapat Melakukan Persetujuan Dengan Metode Ini')
        return redirect('/dokumentasi/list/pola-rules')


@login_required
@check_device
@permissions(role=['depdirbid'])
def approved_depdirbid_pola_rules(request, pk):
    queryset = ProgressVersion.objects.all()
    instance = queryset.get(pk=pk)
    if request.method == 'POST' and instance.is_aju is True and instance.is_approved_asdep is True and instance.is_approved_depdirbid is False:
        instance.is_approved_depdirbid = True
        instance.dt_is_approved_depdirbid = timezone.now()
        instance.open_edit = False
        instance.save()
        messages.success(request, 'Telah Disetujui oleh Depdirbid Versi Pola Rules : 1.{0} Telah Release'.format(
            instance.version))
        return redirect('/dokumentasi/list/pola-rules')
    else:
        messages.info(request, 'Anda Tidak Dapat Melakukan Persetujuan Dengan Metode Ini')
        return redirect('/dokumentasi/list/pola-rules')


@login_required
@check_device
@permissions(role=['entrilogik'])
def open_edit_list_pola_rules(request):
    if request.method == 'POST':
        progressversion = ProgressVersion.objects.all().last()
        if progressversion.is_aju is True and progressversion.is_approved_asdep is True and progressversion.is_approved_depdirbid is True and progressversion.open_edit is False:
            progressversion.open_edit = True
            progressversion.save()
            messages.info(request, 'Anda Sedang Membuka Mode Open Edit')
        else:
            messages.info(request, 'Anda Tidak Dapat Melakukan Open Edit Dengan Metode Ini')
    else:
        messages.info(request, 'Anda Tidak Dapat Melakukan Open Edit Dengan Metode Ini')
    return redirect('/dokumentasi/list/pola-rules')



@login_required
@check_device
@permissions(role=['entrilogik'])
def add_pola_rules_same_version(request):
    queryset = PolaRules.objects.all()
    progressversion = ProgressVersion.objects.all().last()
    version_selected = progressversion.version
    if request.method == 'POST':
        data = request.POST
        los_data = None
        if data.get('los') == '':
            pass
        else:
            los_data = data.get('los')
        usia_data = None
        if data.get('usia') == '':
            pass
        else:
            usia_data = data.get('usia')
        polarules = PolaRules(
            progress_version=progressversion,
            nama_rules=data.get('nama_rules'),
            diagnosis_utama=data.get('diagnosis_utama_combined'),
            diagnosis_sekunder=data.get('diagnosis_sekunder_combined'),
            prosedur=data.get('prosedur_combined'),
            jenis_pelayanan=data.get('jenis_pelayanan'),
            cmg=data.get('cmg'),
            los=los_data,
            cbg=data.get('cbg'),
            severity_level=data.get('severity_level'),
            jenis_kelamin=data.get('jenis_kelamin'),
            usia=usia_data,
            pesan=data.get('pesan'),
            models_polarules=data.get('models_polarules')
        )
        polarules.save()
        messages.info(request, 'Data Pola Rules Entry Logic Sudah Ditambahkan')
        return redirect('/dokumentasi/list/pola-rules')
    context = {
        'queryset': queryset,
        'version_selected': version_selected,
    }
    return render(request, 'dokumentasi/add_pola_rules_same_version.html', context)



@login_required
@check_device
@permissions(role=['asdep', 'depdirbid'])
def reject_pola_rules(request):
    progressversion = ProgressVersion.objects.all().last()
    progressversion.is_aju = False
    progressversion.dt_is_aju = timezone.now()
    progressversion.is_approved_asdep = False
    progressversion.dt_is_approved_asdep = timezone.now()
    progressversion.is_approved_depdirbid = False
    progressversion.dt_is_approved_depdirbid = timezone.now()
    progressversion.open_edit = True
    progressversion.dt_open_edit = timezone.now()
    progressversion.is_rejected = True
    progressversion.dt_is_rejected = timezone.now()
    progressversion.save()
    messages.info(request, 'Pengajuan Pola Rules Telah Dibatalkan')
    return redirect('/dokumentasi/list/pola-rules')