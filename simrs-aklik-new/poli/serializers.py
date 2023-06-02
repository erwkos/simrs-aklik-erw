from django.shortcuts import get_object_or_404
from django.db import transaction

from rest_framework import serializers

from .models import KondisiPasien
from pasien.models import Antrian
from icd.models import ICDX as MasterDataICDX
from icd.models import ICD9 as MasterDataICD9
from .models import (
    ICDX,
    ICD9,
    LayananEdukasi,
    LayananEdukasiPasien,
    LayananMonitoring,
    LayananMonitoringPasien,
    LayananTindakan,
    LayananTindakanPasien,
    LayananKonsultasi,
    LayananKonsultasiPasien
)
from farmasi.models import(
    Obat,
    ObatPasien
)
from radiologi.models import LayananRadiologi, LayananRadiologiPasien
from lab.models import LayananLab, LayananLabPasien


class AntrianPoliSerializer(serializers.ModelSerializer):

    class Meta:
        model = Antrian
        fields = '__all__'


class KondisiPasienSerializer(serializers.ModelSerializer):
    antrian = serializers.IntegerField(required=True)
    perawat = serializers.IntegerField(read_only=True)

    class Meta:
        model = KondisiPasien
        fields = '__all__'

    def validate(self, attrs):
        attrs = super(KondisiPasienSerializer, self).validate(attrs)
        if KondisiPasien.objects.filter(antrian__id=attrs.get('antrian')).exists():
            raise serializers.ValidationError({'antrian': ['Antrian sudah memiliki data kondisi pasien.']})
        return attrs

    def create(self, data):
        antrian = get_object_or_404(Antrian, id=data.get('antrian'))
        data['antrian'] = antrian
        data['dokter'] = antrian.pendaftaran.dokter
        kondisi_pasien = super(KondisiPasienSerializer, self).create(data)
        return kondisi_pasien

    def to_representation(self, instance):
        return {
            'success': True
        }


class UpdateKondisiPasienSerializer(serializers.ModelSerializer):

    class Meta:
        model = KondisiPasien
        exclude = [
            'antrian',
            'perawat'
        ]


class ICDXSerializer(serializers.ModelSerializer):
    antrian = serializers.IntegerField(required=True)
    dokter = serializers.IntegerField(read_only=True)
    perawat = serializers.IntegerField(read_only=True)
    kode_icdx = serializers.CharField()

    class Meta:
        model = ICDX
        fields = [
            'antrian',
            'dokter',
            'perawat',
            'kode_icdx'
        ]

    @transaction.atomic
    def create(self, data):
        antrian = get_object_or_404(Antrian, id=data.get('antrian'))
        idcx = get_object_or_404(MasterDataICDX, kode=data.get('kode_icdx'))
        data.pop('kode_icdx')
        data['antrian'] = antrian
        data['dokter'] = antrian.pendaftaran.dokter
        data['icdx'] = idcx
        data['nama'] = idcx.nama
        data['kode'] = idcx.kode
        instance = super(ICDXSerializer, self).create(data)
        return instance

    def to_representation(self, instance):
        return {
            'success': True
        }


class ICD9Serializer(serializers.ModelSerializer):
    antrian = serializers.IntegerField()
    dokter = serializers.IntegerField(read_only=True)
    perawat = serializers.IntegerField(read_only=True)
    kode_icd9 = serializers.CharField()

    class Meta:
        model = ICD9
        fields = [
            'antrian',
            'dokter',
            'perawat',
            'kode_icd9'
        ]


    @transaction.atomic
    def create(self, data):
        antrian = get_object_or_404(Antrian, id=data.get('antrian'))
        idc9 = get_object_or_404(MasterDataICD9, kode=data.get('kode_icd9'))
        data.pop('kode_icd9')
        data['antrian'] = antrian
        data['dokter'] = antrian.pendaftaran.dokter
        data['icd9'] = idc9
        data['nama'] = idc9.nama
        data['kode'] = idc9.kode
        instance = super(ICD9Serializer, self).create(data)
        return instance

    def to_representation(self, instance):
        return {
            'success': True
        }


class LayananRadiologiPasienSerializer(serializers.ModelSerializer):
    antrian = serializers.IntegerField()
    kuantitas = serializers.IntegerField(min_value=1)
    layanan_radiologi = serializers.IntegerField()

    class Meta:
        model = LayananRadiologiPasien
        fields = [
            'antrian',
            'kuantitas',
            'layanan_radiologi'
        ]

    def create(self, data):
        antrian = get_object_or_404(Antrian, id=data.get('antrian'))
        layanan_radiologi = get_object_or_404(LayananRadiologi, id=data.get('layanan_radiologi'))
        data['antrian'] = antrian
        data['layanan_radiologi'] = layanan_radiologi
        data['harga'] = layanan_radiologi.harga
        data['total_harga'] = layanan_radiologi.harga * data.get('kuantitas')
        instance = super(LayananRadiologiPasienSerializer, self).create(data)
        return instance

    def to_representation(self, instance):
        return {
            'success': True
        }


class LayananLabPasienSerializer(serializers.ModelSerializer):
    antrian = serializers.IntegerField()
    kuantitas = serializers.IntegerField(min_value=1)
    layanan_lab = serializers.IntegerField()

    class Meta:
        model = LayananLabPasien
        fields = [
            'antrian',
            'layanan_lab',
            'kuantitas'
        ]

    def create(self, data):
        antrian = get_object_or_404(Antrian, id=data.get('antrian'))
        layanan_lab = get_object_or_404(LayananLab, id=data.get('layanan_lab'))
        data['antrian'] = antrian
        data['dokter'] = antrian.pendaftaran.dokter
        data['layanan_lab'] = layanan_lab
        data['harga'] = layanan_lab.harga
        data['total_harga'] = layanan_lab.harga * data.get('kuantitas')
        instance = super(LayananLabPasienSerializer, self).create(data)
        return instance

    def to_representation(self, instance):
        return {
            'success': True
        }


class EdukasiPasienSerializer(serializers.ModelSerializer):
    antrian = serializers.IntegerField()
    kuantitas = serializers.IntegerField()
    layanan_edukasi = serializers.IntegerField()

    class Meta:
        model = LayananEdukasiPasien
        fields = [
            'antrian',
            'kuantitas',
            'layanan_edukasi'
        ]

    def create(self, data):
        antrian = get_object_or_404(Antrian, id=data.get('antrian'))
        layanan_edukasi = get_object_or_404(LayananEdukasi, id=data.get('layanan_edukasi'))
        data['layanan_edukasi'] = layanan_edukasi
        data['antrian'] = antrian
        data['dokter'] = antrian.pendaftaran.dokter
        data['harga'] = layanan_edukasi.harga
        data['total_harga'] = layanan_edukasi.harga * data.get('kuantitas')
        instance = super(EdukasiPasienSerializer, self).create(data)
        return instance

    def to_representation(self, instance):
        return {
            'success': True
        }


class MonitoringPasienSerializer(serializers.ModelSerializer):
    antrian = serializers.IntegerField()
    kuantitas = serializers.IntegerField()
    layanan_monitoring = serializers.IntegerField()

    class Meta:
        model = LayananMonitoringPasien
        fields = [
            'antrian',
            'kuantitas',
            'layanan_monitoring'
        ]

    def create(self, data):
        antrian = get_object_or_404(Antrian, id=data.get('antrian'))
        layanan_monitoring = get_object_or_404(LayananMonitoring, id=data.get('layanan_monitoring'))
        data['layanan_monitoring'] = layanan_monitoring
        data['antrian'] = antrian
        data['dokter'] = antrian.pendaftaran.dokter
        data['harga'] = layanan_monitoring.harga
        data['total_harga'] = layanan_monitoring.harga * data.get('kuantitas')
        instance = super(MonitoringPasienSerializer, self).create(data)
        return instance

    def to_representation(self, instance):
        return {
            'success': True
        }


class TindakanPasienSerializer(serializers.ModelSerializer):
    antrian = serializers.IntegerField()
    kuantitas = serializers.IntegerField(min_value=1)
    layanan_tindakan = serializers.IntegerField()

    class Meta:
        model = LayananTindakanPasien
        fields = [
            'antrian',
            'kuantitas',
            'layanan_tindakan'
        ]

    def create(self, data):
        antrian = get_object_or_404(Antrian, id=data.get('antrian'))
        layanan_tindakan = get_object_or_404(LayananTindakan, id=data.get('layanan_tindakan'))
        data['layanan_tindakan'] = layanan_tindakan
        data['antrian'] = antrian
        data['dokter'] = antrian.pendaftaran.dokter
        data['harga'] = layanan_tindakan.harga
        data['total_harga'] = layanan_tindakan.harga * data.get('kuantitas')
        instance = super(TindakanPasienSerializer, self).create(data)
        return instance

    def to_representation(self, instance):
        return {
            'success': True
        }


class KonsultasiPasienSerializer(serializers.ModelSerializer):
    antrian = serializers.IntegerField()
    kuantitas = serializers.IntegerField()
    konsultasi = serializers.IntegerField()

    class Meta:
        model = LayananKonsultasiPasien
        fields = [
            'antrian',
            'kuantitas',
            'konsultasi'
        ]

    def create(self, data):
        antrian = get_object_or_404(Antrian, id=data.get('antrian'))
        konsultasi = get_object_or_404(LayananKonsultasi, id=data.get('konsultasi'))
        data['konsultasi'] = konsultasi
        data['antrian'] = antrian
        data['dokter'] = antrian.pendaftaran.dokter
        data['harga'] = konsultasi.harga
        data['total_harga'] = konsultasi.harga * data.get('kuantitas')
        instance = super(KonsultasiPasienSerializer, self).create(data)
        return instance

    def to_representation(self, instance):
        return {
            'success': True
        }


class ObatPasienSerializer(serializers.ModelSerializer):
    antrian = serializers.IntegerField()
    obat = serializers.IntegerField()
    kuantitas = serializers.IntegerField(min_value=1)

    class Meta:
        model = ObatPasien
        fields = [
            'antrian',
            'obat',
            'kuantitas'
        ]

    def create(self, data):
        antrian = get_object_or_404(Antrian, id=data.get('antrian'))
        obat = get_object_or_404(Obat, id=data.get('obat'))
        data['obat'] = obat
        data['antrian'] = antrian
        data['dokter'] = antrian.pendaftaran.dokter
        data['harga'] = obat.harga
        data['kuantitas'] = data.get('kuantitas')
        data['total_harga'] = obat.harga * data.get('kuantitas')
        instance = super(ObatPasienSerializer, self).create(data)
        return instance

    def to_representation(self, instance):
        return {
            'success': True
        }


class DataKondisiPasienSerializer(serializers.ModelSerializer):

    class Meta:
        model = KondisiPasien
        fields = '__all__'


class DataICDXPasienSerializer(serializers.ModelSerializer):

    class Meta:
        model = ICDX
        fields = '__all__'


class DataICD9PasienSerializer(serializers.ModelSerializer):

    class Meta:
        model = ICD9
        fields = '__all__'


class DataLayananRadiologiPasienSerializer(serializers.ModelSerializer):

    class Meta:
        model = LayananRadiologiPasien
        fields = '__all__'


class DataLayananLabPasienSerializer(serializers.ModelSerializer):

    class Meta:
        model = LayananLabPasien
        fields = '__all__'


class DataEdukasiPasienSerializer(serializers.ModelSerializer):

    class Meta:
        model = LayananEdukasiPasien
        fields = '__all__'


class DataMonitoringPasienSerializer(serializers.ModelSerializer):

    class Meta:
        model = LayananMonitoringPasien
        fields = '__all__'


class DataLayananTindakanPasien(serializers.ModelSerializer):

    class Meta:
        model = LayananTindakanPasien
        fields = '__all__'


class DataLayananKonsultasiPasien(serializers.ModelSerializer):

    class Meta:
        model = LayananKonsultasiPasien
        fields = '__all__'


class DetailAssessmentSerializer(serializers.ModelSerializer):
    kondisi_pasien = serializers.SerializerMethodField()
    icdx = serializers.SerializerMethodField()
    icd9 = serializers.SerializerMethodField()
    layanan_radiologi = serializers.SerializerMethodField()
    layanan_lab = serializers.SerializerMethodField()
    layanan_edukasi = serializers.SerializerMethodField()
    layanan_monitoring = serializers.SerializerMethodField()
    layanan_tindakan = serializers.SerializerMethodField()
    layanan_konsultasi = serializers.SerializerMethodField()

    class Meta:
        model = Antrian
        fields = [
            'id',
            'kondisi_pasien',
            'icdx',
            'icd9',
            'layanan_radiologi',
            'layanan_lab',
            'layanan_edukasi',
            'layanan_monitoring',
            'layanan_tindakan',
            'layanan_konsultasi'
        ]

    def get_kondisi_pasien(self, obj):
        kondisi_pasien = KondisiPasien.objects.filter(antrian=obj)
        if kondisi_pasien.exists():
            return DataKondisiPasienSerializer(instance=kondisi_pasien.last()).data
        return None

    def get_icdx(self, obj):
        return DataICDXPasienSerializer(ICDX.objects.filter(antrian=obj), many=True).data

    def get_icd9(self, obj):
        return DataICD9PasienSerializer(ICD9.objects.filter(antrian=obj), many=True).data

    def get_layanan_radiologi(self, obj):
        return DataLayananRadiologiPasienSerializer(LayananRadiologiPasien.objects.filter(antrian=obj), many=True).data

    def get_layanan_lab(self, obj):
        return DataLayananLabPasienSerializer(LayananLabPasien.objects.filter(antrian=obj), many=True).data

    def get_layanan_edukasi(self, obj):
        return DataEdukasiPasienSerializer(LayananEdukasiPasien.objects.filter(antrian=obj), many=True).data

    def get_layanan_monitoring(self, obj):
        return DataMonitoringPasienSerializer(LayananMonitoringPasien.objects.filter(antrian=obj), many=True).data

    def get_layanan_tindakan(self, obj):
        return DataLayananTindakanPasien(LayananTindakanPasien.objects.filter(antrian=obj), many=True).data

    def get_layanan_konsultasi(self, obj):
        return DataLayananKonsultasiPasien(LayananKonsultasiPasien.objects.filter(antrian=obj), many=True).data