from rest_framework import serializers
from .models import PolaRules


class PolaRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolaRules
        fields = '__all__'
