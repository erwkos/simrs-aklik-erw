import django_filters

from klaim.models import DataKlaimCBG


class DataKlaimCBGFilter(django_filters.FilterSet):

    class Meta:
        model = DataKlaimCBG
        fields = ['JNSPEL', 'status']

