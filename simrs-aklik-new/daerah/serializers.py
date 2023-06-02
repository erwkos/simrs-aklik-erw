

from rest_framework import serializers

from .models import (
    Provinsi,
    Kabupaten,
    Kecamatan,
    Daerah
)


class KecamatanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Kecamatan
        fields = ['nama']
