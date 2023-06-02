from django.shortcuts import render, get_object_or_404, redirect

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.views.generic import View, DetailView
from django.db.models import Q
from django.views.generic import CreateView
#
from datetime import datetime
#
from .models import (
    # ICDX,
    ICD9,
    # LayananEdukasiPasien,
    # LayananMonitoringPasien,
    # LayananKonsultasiPasien,
    # LayananTindakanPasien
)
from antrian.models import Antrian
# from .models import KondisiPasien
# from .serializers import (
#     KondisiPasienSerializer,
#     UpdateKondisiPasienSerializer,
#     ICDXSerializer,
#     ICD9Serializer,
#     LayananRadiologiPasienSerializer,
#     LayananLabPasienSerializer,
#     EdukasiPasienSerializer,
#     MonitoringPasienSerializer,
#     TindakanPasienSerializer,
#     DetailAssessmentSerializer,
#     ObatPasienSerializer,
#     KonsultasiPasienSerializer,
#     AntrianPoliSerializer,
# )
# from radiologi.models import LayananRadiologiPasien, LayananRadiologi
# from lab.models import LayananLabPasien, LayananLab
#
#
# class PoliViewSet(GenericViewSet):
#     serializer_class = KondisiPasienSerializer
#     lookup_field = 'id'
#
#     def get_object(self):
#         if self.action == 'retrieve':
#             return get_object_or_404(Antrian, id=self.kwargs.get('id'))
#         elif self.action == 'update_kondisi_pasien':
#             return get_object_or_404(KondisiPasien, id=self.kwargs.get('id'))
#         return super(PoliViewSet, self).get_object()
#
#     def get_serializer_class(self):
#         if self.action == 'icdx':
#             return ICDXSerializer
#         elif self.action == 'icd9':
#             return ICD9Serializer
#         elif self.action == 'layanan_radiologi':
#             return LayananRadiologiPasienSerializer
#         elif self.action == 'layanan_lab':
#             return LayananLabPasienSerializer
#         elif self.action == 'layanan_edukasi':
#             return EdukasiPasienSerializer
#         elif self.action == 'layanan_monitoring':
#             return MonitoringPasienSerializer
#         elif self.action == 'layanan_tindakan':
#             return TindakanPasienSerializer
#         elif self.action == 'konsultasi':
#             return KonsultasiPasienSerializer
#         elif self.action == 'obat':
#             return ObatPasienSerializer
#         elif self.action == 'retrieve':
#             return DetailAssessmentSerializer
#         elif self.action == 'update_kondisi_pasien':
#             return UpdateKondisiPasienSerializer
#         return super(PoliViewSet, self).get_serializer_class()
#
#     @action(methods=['POST'], detail=False)
#     def kondisi_pasien(self, request):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_302_FOUND, headers={'Location': f'/poli/assessment/{request.data.get("antrian")}'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     @action(methods=['POST'], detail=False)
#     def icdx(self, request):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_302_FOUND, headers={'Location': f'/poli/assessment/{request.data.get("antrian")}'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     @action(methods=['POST'], detail=False)
#     def delete_icdx(self, request):
#         icdx = get_object_or_404(ICDX, id=request.data.get('icdx'))
#         icdx.delete()
#         return Response({'success': True}, status=status.HTTP_200_OK)
#
#     @action(methods=['POST'], detail=False)
#     def icd9(self, request):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_302_FOUND, headers={'Location': f'/poli/assessment/{request.data.get("antrian")}'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     @action(methods=['POST'], detail=False)
#     def delete_icd9(self, request):
#         icdx = get_object_or_404(ICD9, id=request.data.get('icd9'))
#         icdx.delete()
#         return Response({'success': True}, status=status.HTTP_200_OK)
#
#     @action(methods=['POST'], detail=False)
#     def layanan_radiologi(self, request):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_302_FOUND, headers={'Location': f'/poli/assessment/{request.data.get("antrian")}'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     @action(methods=['POST'], detail=False)
#     def delete_layanan_radiologi(self, request):
#         instance = get_object_or_404(LayananRadiologiPasien, id=request.data.get('layanan_radiologi'))
#         instance.delete()
#         return Response({'success': True}, status=status.HTTP_200_OK)
#
#     @action(methods=['POST'], detail=False)
#     def layanan_lab(self, request):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_302_FOUND, headers={'Location': f'/poli/assessment/{request.data.get("antrian")}'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     @action(methods=['POST'], detail=False)
#     def delete_layanan_lab(self, request):
#         instance = get_object_or_404(LayananLabPasien, id=request.data.get('layanan_lab'))
#         instance.delete()
#         return Response({'success': True}, status=status.HTTP_200_OK)
#
#     @action(methods=['POST'], detail=False)
#     def layanan_edukasi(self, request):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_302_FOUND, headers={'Location': f'/poli/assessment/{request.data.get("antrian")}'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     @action(methods=['POST'], detail=False)
#     def delete_layanan_edukasi(self, request):
#         instance = get_object_or_404(LayananEdukasiPasien, id=request.data.get('layanan_edukasi'))
#         instance.delete()
#         return Response({'success': True}, status=status.HTTP_200_OK)
#
#     @action(methods=['POST'], detail=False)
#     def layanan_monitoring(self, request):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_302_FOUND, headers={'Location': f'/poli/assessment/{request.data.get("antrian")}'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     @action(methods=['POST'], detail=False)
#     def delete_layanan_monitoring(self, request):
#         instance = get_object_or_404(LayananMonitoringPasien, id=request.data.get('layanan_monitoring'))
#         instance.delete()
#         return Response({'success': True}, status=status.HTTP_200_OK)
#
#     @action(methods=['POST'], detail=False)
#     def layanan_tindakan(self, request):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status.HTTP_302_FOUND, headers={'Location': f'/poli/assessment/{request.data.get("antrian")}'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     @action(methods=['POST'], detail=False)
#     def delete_layanan_tindakan(self, request):
#         instance = get_object_or_404(LayananTindakanPasien, id=request.data.get('layanan_tindakan'))
#         instance.delete()
#         return Response({'success': True}, status=status.HTTP_200_OK)
#
#     @action(methods=['POST'], detail=False)
#     def obat(self, request):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_302_FOUND, headers={'Location': f'/poli/assessment/{request.data.get("antrian")}'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     @action(methods=['POST'], detail=False)
#     def konsultasi(self, request):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_302_FOUND, headers={'Location': f'/poli/assessment/{request.data.get("antrian")}'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     @action(methods=['POST'], detail=False)
#     def delete_konsultasi(self, request):
#         instance = get_object_or_404(LayananKonsultasiPasien, id=request.data.get('layanan_konsultasi'))
#         instance.delete()
#         return Response({'success': True}, status=status.HTTP_200_OK)
#
#     def retrieve(self, request, id):
#         serializer = self.get_serializer(instance=self.get_object())
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     @action(methods=['PUT'], detail=True)
#     def update_kondisi_pasien(self, request, id):
#         serializer = self.get_serializer(instance=self.get_object(), data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
class AntrianPoliView(View):
    template_name = 'poli/antrian-poli.html'

    def get(self, request):
        antrian_list = Antrian.objects.filter(antrian_tanggal=datetime.now())
        antrian_list = antrian_list.filter(Q(task_id=3) | Q(task_id=4))
        context = {
            'antrian_list': antrian_list
        }
        return render(request, self.template_name, context)
#
#
# class AntrianPoliViewSet(GenericViewSet):
#     queryset = Antrian.objects.filter(Q(task_id=3) | Q(task_id=4))
#     serializer_class = AntrianPoliSerializer
#     lookup_field = 'pk'
#
#     def list(self, request):
#         serializer = self.get_serializer(self.get_queryset(), many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#


class HadirAntrianPoliView(View):

    def post(self, request, *args, **kwargs):
        antrian = get_object_or_404(Antrian, id=kwargs.get('antrian'))
        antrian.task_id = 4
        antrian.save()
        return redirect(f'/soap/{antrian.id}')
#
#
# class BatalkanAntrianPoliView(View):
#
#     def post(self, request, *args, **kwargs):
#         antrian = get_object_or_404(Antrian, id=kwargs.get('antrian'))
#         antrian.task_id = 99
#         antrian.save()
#         referer = request.headers.get('Referer')
#         return redirect(referer)
#
#
# class SOAPPoliView(DetailView):
#     queryset = Antrian.objects.all()
#     template_name = 'poli/assessment.html'
#     # template_name = 'admisi/cppt.html'
#
#     def get(self, request, *args, **kwargs):
#         context = self.get_context_data(**kwargs)
#         return render(request, self.template_name, context)
#
#     def get_context_data(self, **kwargs):
#         antrian = get_object_or_404(Antrian, id=kwargs.get('antrian'))
#         return {
#             'antrian': antrian,
#             'pasien': antrian.pendaftaran.pasien,
#             'icd9_list': ICD9.objects.filter(antrian=get_object_or_404(Antrian, id=kwargs.get('antrian'))),
#             'kondisi_pasien': KondisiPasien.objects.filter(antrian=get_object_or_404(Antrian, id=kwargs.get('antrian'))).first(),
#             'layanan_radiologi': LayananRadiologi.objects.all(),
#             'layanan_radiologi_pasien': LayananRadiologiPasien.objects.filter(antrian=get_object_or_404(Antrian, id=kwargs.get('antrian'))),
#             'layanan_lab': LayananLab.objects.all(),
#             'layanan_lab_pasien': LayananLabPasien.objects.filter(antrian=antrian)
#         }
#
#
# class KondisiPasienView(CreateView):
#     queryset = Antrian.objects.all()
#     pk_url_kwarg = 'pk'
#
#     def post(self, request, *args, **kwargs):
#         antrian = self.get_object(self.get_queryset())
#         kondisi_pasien = KondisiPasien.objects.filter(antrian=antrian)
#         data = request.POST
#         if kondisi_pasien.exists():
#             kondisi_pasien = kondisi_pasien.first()
#             kondisi_pasien.keluhan_utama = data.get('keluhan_utama')
#             kondisi_pasien.kondisi_umum = data.get('kondisi_umum')
#             kondisi_pasien.riwayat_penyakit_dahulu = data.get('riwayat_penyakit_dahulu')
#             kondisi_pasien.riwayat_penyakit_sekarang = data.get('riwayat_penyakit_sekarang')
#             kondisi_pasien.kesadaran = data.get('kesadaran')
#             kondisi_pasien.tensi_sistol = data.get('tensi_sistol')
#             kondisi_pasien.tensi_diastol = data.get('tensi_diastol')
#             kondisi_pasien.nadi = data.get('nadi')
#             kondisi_pasien.rr = data.get('rr')
#             kondisi_pasien.suhu = data.get('suhu')
#             kondisi_pasien.down_score = data.get('down_score')
#             kondisi_pasien.trauma_score = data.get('trauma_score')
#             kondisi_pasien.meows_score = data.get('meows_score')
#             kondisi_pasien.berat_badan = data.get('berat_badan')
#             kondisi_pasien.tinggi_badan = data.get('tinggi_badan')
#             kondisi_pasien.gcs_e = data.get('gcs_e')
#             kondisi_pasien.gcs_m = data.get('gcs_m')
#             kondisi_pasien.gcs_v = data.get('gcs_v')
#             kondisi_pasien.kepala = data.get('kepala')
#             kondisi_pasien.mata = data.get('mata')
#             kondisi_pasien.telinga = data.get('telinga')
#             kondisi_pasien.hidung = data.get('hidung')
#             kondisi_pasien.gigi = data.get('gigi')
#             kondisi_pasien.mulut = data.get('mulut')
#             kondisi_pasien.leher = data.get('leher')
#             kondisi_pasien.wajah = data.get('wajah')
#             kondisi_pasien.thorax = data.get('thorax')
#             kondisi_pasien.paru_paru = data.get('paru_paru')
#             kondisi_pasien.jantung = data.get('jantung')
#             kondisi_pasien.abdomen = data.get('abdomen')
#             kondisi_pasien.hati = data.get('hati')
#             kondisi_pasien.limpa = data.get('limpa')
#             kondisi_pasien.generalia = data.get('generalia')
#             kondisi_pasien.ekstrimitas = data.get('ekstrimitas')
#             kondisi_pasien.status_lokalis = data.get('status_lokalis')
#
#             kondisi_pasien.rencana_tindakan = data.get('rencana_tindakan')
#             kondisi_pasien.terapi_obat_obatan = data.get('terapi_obat_obatan')
#             kondisi_pasien.rencana_konsultasi = data.get('rencana_konsultasi')
#             kondisi_pasien.rencana_rawat = data.get('rencana_rawat')
#             kondisi_pasien.rencana_perawatan_pasca_rawat = data.get('rencana_perawatan_pasca_rawat')
#             kondisi_pasien.keadaan_keluar = data.get('keadaan_keluar')
#             kondisi_pasien.cara_keluar = data.get('cara_keluar')
#             kondisi_pasien.pemeriksaan_lanjutan = data.get('pemeriksaan_lanjutan')
#             kondisi_pasien.save()
#         else:
#             KondisiPasien.objects.create(
#                 antrian=antrian,
#                 dokter=antrian.pendaftaran.dokter,
#                 keluhan_utama=data.get('keluhan_utama'),
#                 kondisi_umum=data.get('kondisi_umum'),
#                 riwayat_penyakit_dahulu=data.get('riwayat_penyakit_dahulu'),
#                 riwayat_penyakit_sekarang=data.get('riwayat_penyakit_sekarang'),
#                 kesadaran=data.get('kesadaran'),
#                 tensi_sistol=data.get('tensi_sistol'),
#                 tensi_diastol=data.get('tensi_diastol'),
#                 nadi=data.get('nadi', 'tidak ada'),
#                 isi=data.get('isi', 'tidak ada'),
#                 rr=data.get('rr', 'tidak ada'),
#                 suhu=data.get('suhu'),
#                 down_score=data.get('down_score'),
#                 trauma_score=data.get('trauma_score'),
#                 meows_score=data.get('meows_score'),
#                 berat_badan=data.get('berat_badan'),
#                 tinggi_badan=data.get('tinggi_badan'),
#                 gcs_e=data.get('gcs_e'),
#                 gcs_m=data.get('gcs_m'),
#                 gcs_v=data.get('gcs_v'),
#                 kepala=data.get('kepala'),
#                 mata=data.get('mata'),
#                 telinga=data.get('telinga'),
#                 hidung=data.get('hidung'),
#                 gigi=data.get('gigi'),
#                 mulut=data.get('mulut'),
#                 leher=data.get('leher'),
#                 wajah=data.get('wajah'),
#                 thorax=data.get('thorax'),
#                 paru_paru=data.get('paru_paru'),
#                 jantung=data.get('jantung'),
#                 abdomen=data.get('abdomen'),
#                 hati=data.get('hati'),
#                 limpa=data.get('limpa'),
#                 generalia=data.get('generalia'),
#                 ekstrimitas=data.get('ekstrimitas', 'tidak ada'),
#                 status_lokalis=data.get('status_lokalis')
#             )
#         return redirect(f'/poli/soap/{antrian.id}')