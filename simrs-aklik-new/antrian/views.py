from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import CreateView

from datetime import datetime
import uuid

from antrian.models import Loket, Antrian
from faskes.models import Profil
from .choices import (
    StatusPembayaranChoices
)


class AmbilAntrianView(CreateView):

    def post(self, request, *args, **kwargs):
        data = request.POST
        antrian = Antrian.objects.create(
            no_antrian=Antrian.generate_no_antrian(tanggal_periksa=data.get('tanggal_periksa') or datetime.now()),
            tanggal_periksa=data.get('tanggal_periksa') or datetime.now(),
            antrian_tanggal=datetime.now()
        )
        referer = request.headers.get('Referer')
        return redirect(referer)


class HadirAntrianAdmisiView(CreateView):
    queryset = Antrian.objects.all()
    pk_url_kwarg = 'pk'

    def post(self, request, *args, **kwargs):
        antrian = self.get_object(self.get_queryset())
        antrian.task_id = 2
        antrian.save()
        return redirect(f'/admisi/pendaftaran/rawat-jalan/{antrian.id}')


# Create your views here.
def mesinantrian(request):
    if Profil.objects.filter(id=1).exists():
        profil = Profil.objects.get(id=1)
    else:
        profil = None
    context = {
        "profil": profil,
    }
    return render(request, 'antrian/mesin-antrian.html', context)


def pemanggilantrian(request):
    if Profil.objects.filter(id=1).exists():
        profil = Profil.objects.get(id=1)
    else:
        profil = None
    loket = Loket.objects.all()
    antrian = Antrian.objects.filter(antrian_tanggal=datetime.now(), task_id=1).order_by('-id')
    loketanda = Loket.objects.filter(petugas_admisi=request.user).first()
    context = {
        "profil": profil,
        "loketanda": loketanda,
        "antrian": antrian,
    }
    return render(request, 'antrian/pemanggil-antrian.html', context)


def claimantrian(request):
    antrian = Antrian.objects.get(id=request.POST.get('id'))
    loket = Loket.objects.get(petugas_admisi=request.user)
    antrian.loket = loket
    antrian.save()
    return redirect('pemanggilantrian')


def batalkanantrian(request):
    antrian = Antrian.objects.get(id=request.POST.get('id'))
    antrian.task_id = 99
    antrian.save()
    antrian.pendaftaran.status_pembayaran = StatusPembayaranChoices.BATAL
    antrian.pendaftaran.save()
    return redirect('pemanggilantrian')


def pilihloket(request):
    if Loket.objects.filter(petugas_admisi=request.user).exists():
        loketanda = Loket.objects.get(petugas_admisi=request.user)
        loketanda.nama = request.POST.get('loket')
        loketanda.save()
        return redirect('pemanggilantrian')
    else:
        buatloket = Loket(
            kode=uuid.uuid4(),
            loket=request.POST.get('loket'),
            petugas_admisi=request.user
        )
        buatloket.save()
        return redirect('pemanggilantrian')


@login_required
def automengantri(request):
    waktusekarang = datetime.now()
    antrian = Antrian.objects.filter(antrian_tanggal=datetime.now()).order_by('id')
    if antrian.exists():
        nomor_sekarang = antrian.last().no_antrian
    else:
        nomor_sekarang = 0
    no_antrian = nomor_sekarang + 1
    context = {
        'waktusekarang': waktusekarang,
        'antrian': antrian,
        'hitungantrian1': no_antrian,
    }
    return render(request, 'snippets/automengantri.html', context)


@login_required
def autowaktusekarang(request):
    data = datetime.now()
    return render(request, 'snippets/autowaktusekarang.html', {"data": data})
