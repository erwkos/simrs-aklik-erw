from rest_framework import serializers

from vpkaak.models import RegisterPostKlaim, SamplingDataKlaimCBG
from user.models import User


class RegisterPostKlaimSerializer(serializers.ModelSerializer):
    faskes = serializers.SerializerMethodField()

    class Meta:
        model = RegisterPostKlaim
        fields = '__all__'

    def get_faskes(self, obj):
        return obj.user.kantorcabang_set.all().first().kode_cabang


class SamplingDataKlaimCBGSerializer(serializers.ModelSerializer):
    faskes = serializers.SerializerMethodField()

    class Meta:
        model = SamplingDataKlaimCBG
        fields = '__all__'

    def get_faskes(self, obj):
        return obj.faskes.nama


#
# class VerifikatorSerializer(serializers.ModelSerializer):
#     fullname = serializers.SerializerMethodField()
#
#     class Meta:
#         model = User
#         fields = ['id', 'fullname']
#
#     def get_fullname(self, obj):
#         return obj.get_full_name()
#

class RegisterPostKlaimSupervisorKPSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterPostKlaim
        fields = '__all__'
