from django.shortcuts import get_object_or_404

from rest_framework import serializers

from .models import LayananRadiologi, LayananRadiologiPasien
from pasien.models import Antrian


class LayananRadiologiPasienSerializer(serializers.ModelSerializer):
    kuantitas = serializers.IntegerField(min_value=1)
    layanan_radiologi = serializers.IntegerField()

    class Meta:
        model = LayananRadiologiPasien
        fields = [
            'antrian',
            'kuantitas'
        ]

    def create(self, data):
        antrian = get_object_or_404(Antrian, id=data.get('antrian'))
        layanan_radiologi = get_object_or_404(LayananRadiologi, id=data.get('layanan_radiologi'))
        data['antrian'] = layanan_radiologi
        data['harga'] = layanan_radiologi.harga
        data['total_harga'] = layanan_radiologi.harga * data.get('kuantitas')
        instance = super(LayananRadiologiPasienSerializer, self).create(data)
        return instance

    def to_representation(self, instance):
        return {
            'success': True
        }


