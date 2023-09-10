

from rest_framework import serializers

from klaim.models import (
    RegisterKlaim,
    DataKlaimCBG
)
from user.models import User


class RegisterKlaimSerializer(serializers.ModelSerializer):
    faskes = serializers.SerializerMethodField()

    class Meta:
        model = RegisterKlaim
        fields = '__all__'

    def get_faskes(self, obj):
        return obj.faskes.nama


class DataKlaimSerializer(serializers.ModelSerializer):
    faskes = serializers.SerializerMethodField()

    class Meta:
        model = DataKlaimCBG
        fields = '__all__'

    def get_faskes(self, obj):
        return obj.faskes.nama


class VerifikatorSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'fullname']

    def get_fullname(self, obj):
        return obj.get_full_name()

