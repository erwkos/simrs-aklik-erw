
from rest_framework import serializers

from .models import Pasien


class PasienSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pasien
        fields = '__all__'
