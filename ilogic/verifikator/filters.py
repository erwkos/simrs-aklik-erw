import django_filters

from faskes.models import Faskes
from klaim.models import DataKlaimCBG
from user.models import User
from django.contrib.auth.models import Group

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
            # 'verifikator',
        ]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)  # Dapatkan 'request' dari kwargs
        super().__init__(*args, **kwargs)

        if request and request.user.is_authenticated:
            # Filter queryset berdasarkan request.user jika pengguna terautentikasi
            self.filters['faskes'].field.queryset = Faskes.objects.filter(kantor_cabang__in=request.user.kantorcabang_set.all())
