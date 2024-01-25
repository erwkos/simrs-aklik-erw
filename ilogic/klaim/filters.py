import django_filters
from dal import autocomplete
from django.forms import NumberInput, DateInput

from faskes.models import Faskes
from klaim.models import RegisterKlaim
from user.models import User
from django.contrib.auth.models import Group


class RegisterKlaimFaskesFilter(django_filters.FilterSet):
    faskes = django_filters.ModelChoiceFilter(queryset=Faskes.objects.all(),
                                              widget=autocomplete.ModelSelect2(
                                                  url='verifikator:rumahsakit-autocomplete',
                                              ))
    bulan_pelayanan_month = django_filters.NumberFilter(field_name='bulan_pelayanan', lookup_expr='month',
                                                        widget=NumberInput(attrs={'min': 1, 'oninput':
                                                            "this.value =!!this.value && Math.abs(this.value) >= 1 ? Math.abs(this.value) : null", }),
                                                        label='Bulan Bupel')
    bulan_pelayanan_year = django_filters.NumberFilter(field_name='bulan_pelayanan', lookup_expr='year',
                                                       widget=NumberInput(attrs={'min': 2023, 'oninput':
                                                           "this.value =!!this.value && Math.abs(this.value) >= 1 ? Math.abs(this.value) : null", }),
                                                       label='Tahun Bupel')

    nomor_register_klaim = django_filters.CharFilter(field_name='nomor_register_klaim', lookup_expr='icontains',
                                                     label='No REG')

    class Meta:
        model = RegisterKlaim
        fields = ['faskes',
                  'jenis_klaim',
                  'status',
                  'verifikator',
                  ]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)  # Dapatkan 'request' dari kwargs
        super().__init__(*args, **kwargs)

        if request and request.user.is_authenticated:
            # Filter queryset berdasarkan request.user jika pengguna terautentikasi
            self.filters['verifikator'].field.queryset = User.objects.filter(
                kantorcabang__in=request.user.kantorcabang_set.all(),
                groups__in=Group.objects.filter(name='verifikator'))


class RegisterKlaimKhususFaskesFilter(django_filters.FilterSet):
    bulan_pelayanan_month = django_filters.NumberFilter(field_name='bulan_pelayanan', lookup_expr='month',
                                                        widget=NumberInput(attrs={'min': 1, 'oninput':
                                                            "this.value =!!this.value && Math.abs(this.value) >= 0 ? Math.abs(this.value) : null", }),
                                                        label='Bulan Bupel')
    bulan_pelayanan_year = django_filters.NumberFilter(field_name='bulan_pelayanan', lookup_expr='year',
                                                       widget=NumberInput(attrs={'min': 2023, 'oninput':
                                                           "this.value =!!this.value && Math.abs(this.value) >= 0 ? Math.abs(this.value) : null", }),
                                                       label='Tahun Bupel')
    tgl_aju_gte = django_filters.DateFilter(field_name='tgl_aju', lookup_expr='date__gte',
                                            widget=DateInput(attrs={'type': 'date'}), label='Tgl Aju Mulai')
    tgl_aju_lte = django_filters.DateFilter(field_name='tgl_aju', lookup_expr='date__lte',
                                            widget=DateInput(attrs={'type': 'date'}), label='Tgl Aju Sampai')

    nomor_register_klaim = django_filters.CharFilter(field_name='nomor_register_klaim', lookup_expr='icontains',
                                                     label='No REG')

    class Meta:
        model = RegisterKlaim
        fields = ['jenis_klaim',
                  'status',
                  ]
