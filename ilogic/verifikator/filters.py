import django_filters

from klaim.models import DataKlaimCBG


class DataKlaimCBGFilter(django_filters.FilterSet):

    class Meta:
        model = DataKlaimCBG
        fields = ['JNSPEL', 'status']


class DownloadDataKlaimCBGFilter(django_filters.FilterSet):
    nomor_register_klaim = django_filters.CharFilter(field_name='register_klaim__nomor_register_klaim')
    bupel_month = django_filters.NumberFilter(field_name='bupel', lookup_expr='month')
    bupel_year = django_filters.NumberFilter(field_name='bupel', lookup_expr='year')

    class Meta:
        model = DataKlaimCBG
        fields = [
            # 'register_klaim',
            'faskes',
            'JNSPEL',
            'status',
            # 'bupel',
            'verifikator',
        ]
