

from rest_framework import serializers

from .models import (
    DataKlaimCBG
)


class MonitoringDataKlaimSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataKlaimCBG
        fields = '__all__'
