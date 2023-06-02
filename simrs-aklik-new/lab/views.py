from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, View
from django.db.models import Q
from django.db import transaction


from .models import (
    LayananLabPasien,
    SubLayananLab,
    HasilSubLayananLab,
    LayananLab

)
from .choices import (
    StatusLayananChoices,
    AsuransiChoices
)
from pasien.models import Antrian


class RequestLayananLabPasienRawatJalan(CreateView):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = request.POST
        antrian = get_object_or_404(Antrian, id=data.get('antrian_id'))
        kuantitas = 1   # default
        for sub_id in data.getlist('sub_id'):
            sub = get_object_or_404(SubLayananLab, id=sub_id)
            layanan_lab_pasien = LayananLabPasien.objects.filter(
                layanan_lab=sub.layanan_lab,
                antrian=antrian,
                status_layanan=StatusLayananChoices.MENUNGGU)
            if not layanan_lab_pasien.exists():
                layanan_lab_pasien = LayananLabPasien.objects.create(
                    antrian=antrian,
                    resume_medis=antrian.pendaftaran.resume_medis,
                    dokter=request.user,
                    layanan_lab=sub.layanan_lab,
                    harga=sub.layanan_lab.harga,
                    total_harga=sub.layanan_lab.harga * kuantitas,
                    summary_invoice=antrian.pendaftaran.summary_invoice)
            else:
                layanan_lab_pasien = layanan_lab_pasien.first()

            if antrian.pendaftaran.asuransi == AsuransiChoices.BPJS:
                layanan_lab_pasien.total_harga = 0
                layanan_lab_pasien.save()

            hasil_layanan_lab = HasilSubLayananLab.objects.create(
                    sub_layanan_lab=sub,
                    layanan_lab_pasien=layanan_lab_pasien
                )
        referer = request.headers.get('Referer')
        return redirect(referer)


class AntrianLabView(ListView):
    queryset = LayananLabPasien.objects.filter(
        Q(status_layanan=StatusLayananChoices.MENUNGGU) | Q(status_layanan=StatusLayananChoices.DILAYANI)
    )
    template_name = 'lab/antrian-lab.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {
            'layanan_lab_pasien_list': self.get_queryset()
        }
        return context


class BatalkanLayananLabPasienView(DetailView):
    queryset = LayananLabPasien.objects.filter(status_layanan=StatusLayananChoices.MENUNGGU)
    pk_url_kwarg = 'pk'

    def post(self, request, *args, **kwargs):
        layanan = self.get_object(self.get_queryset())
        layanan.status_layanan = StatusLayananChoices.BATAL
        layanan.save()
        return redirect('/lab/antrian-lab')


class HadirLayananLabView(DetailView):
    queryset = LayananLabPasien.objects.filter(status_layanan=StatusLayananChoices.MENUNGGU)
    pk_url_kwarg = 'pk'

    def post(self, request, *args, **kwargs):
        layanan = self.get_object(self.get_queryset())
        layanan.status_layanan = StatusLayananChoices.DILAYANI
        layanan.save()
        return redirect(f'/lab/layanan-lab-laporan/{layanan.id}')


class LaporanLayananLabView(DetailView):
    queryset = LayananLabPasien.objects.filter(status_layanan=StatusLayananChoices.DILAYANI)
    template_name = 'lab/laporan-lab.html'
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        layanan = self.get_object(self.get_queryset())
        sub_layanan = HasilSubLayananLab.objects.filter(layanan_lab_pasien=layanan)
        context = {
            'layanan': layanan,
            'sub_layanan': sub_layanan
        }
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        obj = self.get_object(self.get_queryset())
        data = request.POST
        for sub_id in data.getlist('sub_id'):
            sub = get_object_or_404(HasilSubLayananLab, id=sub_id)
            sub.hasil = data.get(f'hasil_{sub_id}')
            sub.save()
        obj.catatan = data.get('catatan')
        obj.petugas_lab = request.user
        obj.save()
        referer = request.headers.get('Referer')
        return redirect(referer)


class SelesaiLaporanLayananLabView(CreateView):
    queryset = LayananLabPasien.objects.all()
    pk_url_kwarg = 'pk'

    def post(self, request, *args, **kwargs):
        obj = self.get_object(self.get_queryset())
        obj.status_layanan = StatusLayananChoices.SELESAI
        obj.save()
        return redirect('/lab/antrian-lab')


class HasilLaporanLayananLabPasien(DetailView):
    queryset = LayananLabPasien.objects.all()
    template_name = 'lab/hasil-lab.html'
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        layanan = self.get_object(self.get_queryset())
        hasil_sub = HasilSubLayananLab.objects.filter(layanan_lab_pasien=layanan)
        context = {
            'layanan': layanan,
            'hasil_sub': hasil_sub
        }
        return context