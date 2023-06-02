from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView

from antrian.models import Antrian
from .models import (
    LayananTindakan,
    LayananTindakanPasien,

    LayananEdukasi,
    LayananEdukasiPasien,

    LayananMonitoring,
    LayananMonitoringPasien,

    LayananKonsultasi,
    LayananKonsultasiPasien,
)
from .choices import (
    StatusPembayaranChoices,
    AsuransiChoices
)


class TambahLayananTindakanView(CreateView):
    queryset = LayananTindakanPasien.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.POST
        antrian = get_object_or_404(Antrian, id=data.get('antrian_id'))
        layanan = get_object_or_404(LayananTindakan, id=data.get('layanan_id'))
        kuantitas = 1   # default
        layanan_tidakan = LayananTindakanPasien.objects.create(
            antrian=antrian,
            resume_medis=antrian.pendaftaran.resume_medis,
            dokter=request.user,
            summary_invoice=antrian.pendaftaran.summary_invoice,
            harga=layanan.harga,
            kuantitas=kuantitas,
            total_harga=layanan.harga * kuantitas,
            deskripsi=data.get('deskripsi'),
            layanan_tindakan=layanan
        )
        if layanan_tidakan.antrian.pendaftaran.asuransi == AsuransiChoices.BPJS:
            layanan_tidakan.total_harga = 0
            layanan_tidakan.save()
        referer = request.headers.get('Referer')
        return redirect(referer)


class TambahLayananEdukasiView(CreateView):
    queryset = LayananEdukasiPasien.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.POST
        antrian = get_object_or_404(Antrian, id=data.get('antrian_id'))
        layanan = get_object_or_404(LayananEdukasi, id=data.get('layanan_id'))
        kuantitas = 1   # default
        layanan_edukasi = LayananEdukasiPasien.objects.create(
            antrian=antrian,
            resume_medis=antrian.pendaftaran.resume_medis,
            dokter=request.user,
            summary_invoice=antrian.pendaftaran.summary_invoice,
            harga=layanan.harga,
            kuantitas=kuantitas,
            total_harga=layanan.harga * kuantitas,
            deskripsi=data.get('deskripsi'),
            layanan_edukasi=layanan
        )
        if layanan_edukasi.antrian.pendaftaran.asuransi == AsuransiChoices.BPJS:
            layanan_edukasi.total_harga = 0
            layanan_edukasi.save()
        referer = request.headers.get('Referer')
        return redirect(referer)


class TambahLayananMonitoringView(CreateView):
    queryset = LayananMonitoringPasien.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.POST
        antrian = get_object_or_404(Antrian, id=data.get('antrian_id'))
        layanan = get_object_or_404(LayananMonitoring, id=data.get('layanan_id'))
        kuantitas = 1   # default
        layanan_monitoring = LayananMonitoringPasien.objects.create(
            antrian=antrian,
            resume_medis=antrian.pendaftaran.resume_medis,
            dokter=request.user,
            summary_invoice=antrian.pendaftaran.summary_invoice,
            harga=layanan.harga,
            kuantitas=kuantitas,
            total_harga=layanan.harga * kuantitas,
            deskripsi=data.get('deskripsi'),
            layanan_monitoring=layanan
        )
        if layanan_monitoring.antrian.pendaftaran.asuransi == AsuransiChoices.BPJS:
            layanan_monitoring.total_harga = 0
            layanan_monitoring.save()
        referer = request.headers.get('Referer')
        return redirect(referer)


class TambahLayananKonsultasiView(CreateView):
    queryset = LayananKonsultasiPasien.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.POST
        antrian = get_object_or_404(Antrian, id=data.get('antrian_id'))
        layanan = get_object_or_404(LayananKonsultasi, id=data.get('layanan_id'))
        kuantitas = 1   # default
        layanan_konsultasi = LayananKonsultasiPasien.objects.create(
            antrian=antrian,
            resume_medis=antrian.pendaftaran.resume_medis,
            dokter=request.user,
            summary_invoice=antrian.pendaftaran.summary_invoice,
            harga=layanan.harga,
            kuantitas=kuantitas,
            total_harga=layanan.harga * kuantitas,
            deskripsi=data.get('deskripsi'),
            layanan_konsultasi=layanan
        )
        if layanan_konsultasi.antrian.pendaftaran.asuransi == AsuransiChoices.BPJS:
            layanan_konsultasi.total_harga = 0
            layanan_konsultasi.save()
        referer = request.headers.get('Referer')
        return redirect(referer)


class HapusLayananKonsultasiView(CreateView):
    queryset = LayananKonsultasiPasien.objects.filter(
        status_pembayaran=StatusPembayaranChoices.BELUM_BAYAR
    )
    pk_url_kwarg = 'pk'

    def post(self, request, *args, **kwargs):
        obj = self.get_object(self.get_queryset())
        obj.delete()
        referer = request.headers.get('Referer')
        return redirect(referer)


class HapusLayananMonitoringView(CreateView):
    queryset = LayananMonitoringPasien.objects.filter(
        status_pembayaran=StatusPembayaranChoices.BELUM_BAYAR
    )
    pk_url_kwarg = 'pk'

    def post(self, request, *args, **kwargs):
        obj = self.get_object(self.get_queryset())
        obj.delete()
        referer = request.headers.get('Referer')
        return redirect(referer)


class HapusLayananEdukasiView(CreateView):
    queryset = LayananEdukasiPasien.objects.filter(
        status_pembayaran=StatusPembayaranChoices.BELUM_BAYAR
    )
    pk_url_kwarg = 'pk'

    def post(self, request, *args, **kwargs):
        obj = self.get_object(self.get_queryset())
        obj.delete()
        referer = request.headers.get('Referer')
        return redirect(referer)


class HapusLayananTindakanView(CreateView):
    queryset = LayananTindakanPasien.objects.filter(
        status_pembayaran=StatusPembayaranChoices.BELUM_BAYAR
    )
    pk_url_kwarg = 'pk'

    def post(self, request, *args, **kwargs):
        obj = self.get_object(self.get_queryset())
        obj.delete()
        referer = request.headers.get('Referer')
        return redirect(referer)
