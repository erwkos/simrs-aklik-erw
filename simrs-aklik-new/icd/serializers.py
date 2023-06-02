

from rest_framework import serializers

from .models import (
    ICDX,
    ICD9
)


class ICDXSerializer(serializers.ModelSerializer):

    class Meta:
        model = ICDX
        fields = '__all__'


class ICD9Serializer(serializers.ModelSerializer):
    class Meta:
        model = ICD9
        fields = '__all__'
