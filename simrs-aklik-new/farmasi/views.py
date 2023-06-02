from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.generic import CreateView, ListView, UpdateView, DetailView, TemplateView, View
from django.db.models import Q
from django.db import transaction

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters

from antrian.models import Antrian
from .serializers import (
    AntrianFarmasiSerializer,
    MasterDataObatSerializer
)
from .models import (
    Obat,
    ObatPasien
)
from .choices import (
    StatusPembayaranChoices,
    StatusLayananChoices,
    AsuransiChoices
)


class AntrianFarmasiViewSet(GenericViewSet):
    queryset = Antrian.objects.filter(task_id=5)
    serializer_class = AntrianFarmasiSerializer

    def list(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TambahObatPasienRawatJalanView(CreateView):
    queryset = ObatPasien.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.POST
        antrian = get_object_or_404(Antrian, id=data.get('antrian_id'))
        obat = get_object_or_404(Obat, id=data.get('obat_id'))
        kuantitas = int(data.get('kuantitas'))
        obat_pasien = ObatPasien.objects.create(
            antrian=antrian,
            resume_medis=antrian.pendaftaran.resume_medis,
            dokter=request.user,
            obat=obat,
            harga=obat.harga,
            kuantitas=kuantitas,
            total_harga=obat.harga * kuantitas,
            summary_invoice=antrian.pendaftaran.summary_invoice,
            deskripsi=data.get('deskripsi')
        )
        if obat_pasien.antrian.pendaftaran.asuransi == AsuransiChoices.BPJS:
            obat_pasien.total_harga = 0
            obat_pasien.save()
        referer = request.headers.get('Referer')
        return redirect(referer)


class HapusObatPasienView(CreateView):
    queryset = ObatPasien.objects.filter(
        status_pembayaran=StatusPembayaranChoices.BELUM_BAYAR
    ).filter(Q(status_layanan=StatusLayananChoices.MENUNGGU) | Q(status_layanan=StatusLayananChoices.BATAL))
    pk_url_kwarg = 'pk'

    def post(self, request, *args, **kwargs):
        obj = self.get_object(self.get_queryset())
        obj.delete()
        referer = request.headers.get('Referer')
        return redirect(referer)


class AntrianFarmasiView(ListView):
    queryset = Antrian.objects.filter(
        Q(task_id=5) | Q(task_id=6)
    )
    template_name = 'farmasi/antrian-farmasi.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {
            'antrian_list': self.get_queryset()
        }
        return context


class SiapkanObatPasienView(UpdateView):
    queryset = Antrian.objects.all()
    pk_url_kwarg = 'pk'

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        obj = self.get_object(self.get_queryset())
        obj.task_id = 6
        obj.save()
        for obat_pasien in ObatPasien.objects.filter(antrian=obj):
            obat_pasien.petugas_farmasi = request.user
            obat_pasien.save()
        return redirect(f'/farmasi/detail-obat-pasien/{obj.id}')


class DetailObatPasienView(DetailView, UpdateView):
    queryset = Antrian.objects.all()
    template_name = 'farmasi/detail-obat.html'
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        obj = self.get_object(self.get_queryset())
        context = {
            'obat_pasien': ObatPasien.objects.filter(antrian=obj),
            'antrian': obj
        }
        return context


class KonfirmObatDiterimaView(UpdateView):
    queryset = Antrian.objects.all()
    pk_url_kwarg = 'pk'

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        obj = self.get_object(self.get_queryset())
        obj.task_id = 7
        obj.save()
        for obat in ObatPasien.objects.all():
            obat.status_layanan = StatusLayananChoices.SELESAI
            obat.petugas_farmasi = request.user
            obat.save()
        return redirect('/farmasi/antrian-farmasi')


class ApiMasterDataObatViewSet(GenericViewSet):
    queryset = Obat.objects.all()
    serializer_class = MasterDataObatSerializer
    lookup_field = 'pk'
    filter_backends = [filters.SearchFilter]
    search_fields = ['nama', 'kode']

    def list(self, request):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset())[:10], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        obj = self.get_object()
        serializer = self.get_serializer(instance=obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        serializer = self.get_serializer(instance=self.get_object(), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MasterDataObatView(TemplateView):
    template_name = 'farmasi/master-data/daftar-obat.html'


class MasterDataDetailObatView(TemplateView):
    template_name = 'farmasi/master-data/detail-obat.html'
    
    def get(self, request, *args, **kwargs):
        context = {'pk': kwargs.get('pk')}
        return render(request, self.template_name, context)


class MasterDataTambahObatView(TemplateView):
    template_name = 'farmasi/master-data/tambah-obat.html'

