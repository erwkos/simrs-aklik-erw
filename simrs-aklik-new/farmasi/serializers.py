

from rest_framework import serializers

from pasien.models import Antrian
from .models import (
    Obat
)


class AntrianFarmasiSerializer(serializers.ModelSerializer):

    class Meta:
        model = Antrian
        fields = '__all__'


class MasterDataObatSerializer(serializers.ModelSerializer):
    nama = serializers.CharField(required=True)
    kode = serializers.CharField(required=True)
    harga = serializers.FloatField(min_value=0)
    stok = serializers.IntegerField(min_value=0)

    class Meta:
        model = Obat
        fields = '__all__'


