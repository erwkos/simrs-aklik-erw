# from django.shortcuts import get_object_or_404
#
# from rest_framework import serializers
#
# from radiologi.models import LayananRadiologiPasien
# from lab.models import LayananLabPasien
# from poli.models import (
#     LayananEdukasiPasien,
#     LayananMonitoringPasien,
#     LayananTindakanPasien,
#     LayananKonsultasiPasien
# )
# from pasien.models import Antrian, Pendaftaran
# from .choices import StatusPembayaranChoices
# from pasien.models import Antrian
#
#
# class InvoicePendaftaranPasienSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Pendaftaran
#         fields = [
#             'id',
#             'biaya'
#         ]
#
#
# class InvoiceLayananRadiologiPasienSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = LayananRadiologiPasien
#         fields = '__all__'
#
#
# class InvoiceLayananLabPasienSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = LayananLabPasien
#         fields = '__all__'
#
#
# class InvoiceEdukasiPasienSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = LayananEdukasiPasien
#         fields = '__all__'
#
#
# class InvoiceMonitoringPasienSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = LayananMonitoringPasien
#         fields = '__all__'
#
#
# class InvoiceLayananTindakanPasien(serializers.ModelSerializer):
#
#     class Meta:
#         model = LayananTindakanPasien
#         fields = '__all__'
#
#
# class InvoiceLayananKonsultasiPasien(serializers.ModelSerializer):
#
#     class Meta:
#         model = LayananKonsultasiPasien
#         fields = '__all__'
#
#
# class InvoiceRawatJalanSerializer(serializers.ModelSerializer):
#     layanan_pendaftaran = serializers.SerializerMethodField()
#     layanan_radiologi = serializers.SerializerMethodField()
#     layanan_lab = serializers.SerializerMethodField()
#     layanan_edukasi = serializers.SerializerMethodField()
#     layanan_monitoring = serializers.SerializerMethodField()
#     layanan_tindakan = serializers.SerializerMethodField()
#     layanan_konsultasi = serializers.SerializerMethodField()
#     total_harga = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Antrian
#         fields = [
#             'id',
#             'layanan_pendaftaran',
#             'layanan_radiologi',
#             'layanan_lab',
#             'layanan_edukasi',
#             'layanan_monitoring',
#             'layanan_tindakan',
#             'layanan_konsultasi',
#             'total_harga'
#         ]
#
#     def get_layanan_pendaftaran(self, obj):
#         return InvoicePendaftaranPasienSerializer(obj.pendaftaran).data
#
#     def get_layanan_radiologi(self, obj):
#         return InvoiceLayananRadiologiPasienSerializer(LayananRadiologiPasien.objects.filter(antrian=obj), many=True).data
#
#     def get_layanan_lab(self, obj):
#         return InvoiceLayananLabPasienSerializer(LayananLabPasien.objects.filter(antrian=obj), many=True).data
#
#     def get_layanan_edukasi(self, obj):
#         return InvoiceEdukasiPasienSerializer(LayananEdukasiPasien.objects.filter(antrian=obj), many=True).data
#
#     def get_layanan_monitoring(self, obj):
#         return InvoiceMonitoringPasienSerializer(LayananMonitoringPasien.objects.filter(antrian=obj), many=True).data
#
#     def get_layanan_tindakan(self, obj):
#         return InvoiceLayananTindakanPasien(LayananTindakanPasien.objects.filter(antrian=obj), many=True).data
#
#     def get_layanan_konsultasi(self, obj):
#         return InvoiceLayananKonsultasiPasien(LayananKonsultasiPasien.objects.filter(antrian=obj), many=True).data
#
#     def get_total_harga(self, obj):
#         total = 0
#         total += obj.pendaftaran.biaya
#         for layanan in LayananRadiologiPasien.objects.filter(antrian=obj):
#             total += layanan.total_harga
#         for layanan in LayananLabPasien.objects.filter(antrian=obj):
#             total += layanan.total_harga
#         for layanan in LayananEdukasiPasien.objects.filter(antrian=obj):
#             total += layanan.total_harga
#         for layanan in LayananMonitoringPasien.objects.filter(antrian=obj):
#             total += layanan.total_harga
#         for layanan in LayananTindakanPasien.objects.filter(antrian=obj):
#             total += layanan.total_harga
#         for layanan in LayananKonsultasiPasien.objects.filter(antrian=obj):
#             total += layanan.total_harga
#         return total
#
#
# class BayarInvoiceSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Antrian
#         fields = ['id']
#
#     def update(self, obj, data):
#         antrian = self.context.get('view').get_object()
#         for invoice in LayananRadiologiPasien.objects.filter(antrian=obj):
#             invoice.status_pembayaran = StatusPembayaranChoices.TELAH_DIBAYAR
#             invoice.save()
#         for invoice in LayananLabPasien.objects.filter(antrian=obj):
#             invoice.status_pembayaran = StatusPembayaranChoices.TELAH_DIBAYAR
#             invoice.save()
#         for invoice in LayananEdukasiPasien.objects.filter(antrian=obj):
#             invoice.status_pembayaran = StatusPembayaranChoices.TELAH_DIBAYAR
#             invoice.save()
#         for invoice in LayananMonitoringPasien.objects.filter(antrian=obj):
#             invoice.status_pembayaran = StatusPembayaranChoices.TELAH_DIBAYAR
#             invoice.save()
#         for invoice in LayananTindakanPasien.objects.filter(antrian=obj):
#             invoice.status_pembayaran = StatusPembayaranChoices.TELAH_DIBAYAR
#             invoice.save()
#         for invoice in LayananKonsultasiPasien.objects.filter(antrian=obj):
#             invoice.status_pembayaran = StatusPembayaranChoices.TELAH_DIBAYAR
#             invoice.save()
#         return antrian
#
#     def to_representation(self, instance):
#         return {
#             'success': True
#         }
#
