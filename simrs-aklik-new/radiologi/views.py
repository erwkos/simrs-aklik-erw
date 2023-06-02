from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views.generic import View, ListView, DetailView, CreateView
from django.db import transaction


from .models import LayananRadiologiPasien, LayananRadiologi, FileTracer
from .choices import StatusLayananChoices, AsuransiChoices
from antrian.models import Antrian


class RequestLayananRadiologiPasienRawatJalan(CreateView):

    def post(self, request, *args, **kwargs):
        data = request.POST
        antrian = get_object_or_404(Antrian, id=data.get('antrian_id'))
        layanan_list = LayananRadiologi.objects.filter(id__in=data.getlist('layanan_id'))
        kuantitas = 1   # default kuantitas
        for layanan in layanan_list:
            layanan_pasien = LayananRadiologiPasien.objects.create(
                antrian=antrian,
                dokter=antrian.pendaftaran.dokter,
                resume_medis=antrian.pendaftaran.resume_medis,
                layanan_radiologi=layanan,
                diagnosa=data.get('diagnosa'),
                harga=layanan.harga,
                kuantitas=kuantitas,
                total_harga=layanan.harga * kuantitas,
                summary_invoice=antrian.pendaftaran.summary_invoice)
            if antrian.pendaftaran.asuransi == AsuransiChoices.BPJS:
                layanan_pasien.total_harga = 0
                layanan_pasien.save()
        referer = request.headers.get('Referer')
        return redirect(referer)


class AntrianLayananRadiologiView(ListView):
    queryset = LayananRadiologiPasien.objects.filter(
        Q(status_layanan=StatusLayananChoices.MENUNGGU) | Q(status_layanan=StatusLayananChoices.DILAYANI)
    )
    template_name = 'radiologi/antrian-radiologi.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get_context_data(self, *, object_list=None, **kwargs):
        layanan_radiologi_pasien = self.get_queryset()
        context = {
            'layanan_radiologi_pasien_list': layanan_radiologi_pasien
        }
        return context


class BatalkanLayananRadiologiPasienView(DetailView):
    queryset = LayananRadiologiPasien.objects.filter(status_layanan=StatusLayananChoices.MENUNGGU)
    pk_url_kwarg = 'pk'

    def post(self, request, *args, **kwargs):
        layanan = self.get_object(self.get_queryset())
        layanan.status_layanan = StatusLayananChoices.BATAL
        layanan.save()
        return redirect('/radiologi/antrian-radiologi')


class HadirLayananRadiologiView(DetailView):
    queryset = LayananRadiologiPasien.objects.filter(status_layanan=StatusLayananChoices.MENUNGGU)
    pk_url_kwarg = 'pk'

    def post(self, request, *args, **kwargs):
        layanan = self.get_object(self.get_queryset())
        layanan.status_layanan = StatusLayananChoices.DILAYANI
        layanan.save()
        return redirect(f'/radiologi/layanan-radiologi-laporan/{layanan.id}')


class LaporanLayananRadiologiView(DetailView):
    queryset = LayananRadiologiPasien.objects.filter(status_layanan=StatusLayananChoices.DILAYANI)
    template_name = 'radiologi/laporan-radiologi.html'
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        layanan = self.get_object(self.get_queryset())
        context = {
            'layanan': layanan,
            'file_tracer': FileTracer.objects.filter(layanan_radiologi_pasien=layanan).first()
        }
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        obj = self.get_object(self.get_queryset())
        data = request.POST
        if len(request.FILES.getlist('file_tracer')) > 0:
            for file_tracer in FileTracer.objects.filter(layanan_radiologi_pasien=obj):
                file_tracer.delete()
        for file in request.FILES.getlist('file_tracer'):
            FileTracer.objects.create(
                layanan_radiologi_pasien=obj,
                file=file
            )
        obj.catatan = data.get('catatan')
        obj.petugas_radiologi = request.user
        obj.save()
        referer = request.headers.get('Referer')
        return redirect(referer)


class SelesaiLaporanLayananRadiologi(CreateView):
    queryset = LayananRadiologiPasien.objects.all()
    pk_url_kwarg = 'pk'

    def post(self, request, *args, **kwargs):
        obj = self.get_object(self.get_queryset())
        obj.status_layanan = StatusLayananChoices.SELESAI
        obj.save()
        return redirect('/radiologi/antrian-radiologi')


class HasilLaporanRadiologiPasienView(DetailView):
    queryset = LayananRadiologiPasien.objects.all()
    template_name = 'radiologi/rawat-jalan/hasil-radiologi.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        obj = self.get_object(self.get_queryset())
        file_tracer = FileTracer.objects.filter(
            layanan_radiologi_pasien=obj
        ).first()
        context = {
            'hasil': obj,
            'file_tracer': file_tracer
        }
        return context


