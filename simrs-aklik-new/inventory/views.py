from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView

from .models import AlatKesehatanPasien, AlatKesehatan
from antrian.models import Antrian
from .choices import AsuransiChoices, StatusPembayaranChoices


class TambahLayananMonitoringView(CreateView):
    queryset = AlatKesehatanPasien.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.POST
        antrian = get_object_or_404(Antrian, id=data.get('antrian_id'))
        alat = get_object_or_404(AlatKesehatan, id=data.get('alat_id'))
        kuantitas = int(data.get('kuantitas'))
        alat_pasien = AlatKesehatanPasien.objects.create(
            antrian=antrian,
            resume_medis=antrian.pendaftaran.resume_medis,
            dokter=request.user,
            summary_invoice=antrian.pendaftaran.summary_invoice,
            harga=alat.harga,
            kuantitas=kuantitas,
            total_harga=alat.harga * kuantitas,
            alat=alat
        )
        if alat_pasien.antrian.pendaftaran.asuransi == AsuransiChoices.BPJS:
            alat_pasien.total_harga = 0
            alat_pasien.save()
        referer = request.headers.get('Referer')
        return redirect(referer)


class HapusAlatKesehatanPasienView(UpdateView):
    queryset = AlatKesehatanPasien.objects.filter(status_pembayaran=StatusPembayaranChoices.BELUM_BAYAR)
    pk_url_kwarg = 'pk'

    def post(self, request, *args, **kwargs):
        obj = self.get_object(self.get_queryset())
        obj.delete()
        referer = request.headers.get('Referer')
        return redirect(referer)