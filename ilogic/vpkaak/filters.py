import django_filters
from dal import autocomplete
from django.forms import NumberInput, DateInput
from django_filters import OrderingFilter

from faskes.models import Faskes
from klaim.choices import JenisPelayananChoices
from vpkaak.choices import JenisAuditChoices, StatusChoices, StatusReviewChoices
from vpkaak.models import SamplingDataKlaimCBG, RegisterPostKlaim

STATUS_CHOICES_VERIFIKATOR = (
    ('Proses', 'Proses'),
    ('Layak', 'Layak'),
    ('Pending', 'Pending'),
    ('Dispute', 'Dispute'),
    ('Tidak Layak', 'Tidak Layak'),
)

NMTKP_CHOICES = (
    ('RITL', 'RITL'),
    ('RJTL', 'RJTL'),
)


class RegisterPostKlaimFilter(django_filters.FilterSet):
    nomor_register = django_filters.CharFilter(field_name='nomor_register', lookup_expr='icontains',
                                               label='Nomor Register')
    created_at = django_filters.DateFilter(field_name='created_at', lookup_expr='date', widget=DateInput(attrs={'type': 'date'}),
                                           label='Tanggal Register')
    jenis_audit = django_filters.ChoiceFilter(choices=JenisAuditChoices.choices, label='Jenis Audit')
    status = django_filters.ChoiceFilter(choices=StatusChoices.choices, label='Status')
    nomor_BA_VPK_AAK = django_filters.CharFilter(field_name='nomor_BA_VPK_AAK', lookup_expr='icontains', label='NO BA')

    # class Meta:
    #     model = RegisterPostKlaim
    #     fields = ['nomor_register',
    #               'created_at',
    #               'jenis_audit',
    #               'status',
    #               'nomor_BA_VPK_AAK',
    #               ]


class SamplingDataKlaimCBGFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=StatusReviewChoices.choices, label='Status')
    nomor_register = django_filters.CharFilter(field_name='register__nomor_register', label="No Reg")
    register__jenis_audit = django_filters.ChoiceFilter(choices=JenisAuditChoices.choices, label="Jenis Audit")
    Nosjp = django_filters.CharFilter(field_name='Nosjp', label="No SEP")
    Nmtkp = django_filters.ChoiceFilter(choices=NMTKP_CHOICES, label="NmTKP")

    # o = OrderingFilter(
    #     fields=(
    #         ('status', 'Status'),
    #         ('faskes', 'RS'),
    #         ('register_klaim', 'NO REG'),
    #         ('NOSEP', 'No SEP'),

    #     )
    # )

    # class Meta:
    #     model = DataKlaimCBG
    #     fields = ['status', 'JNSPEL', 'NOSEP']

# class DownloadSamplingDataKlaimCBGFilter(django_filters.FilterSet):
#     nomor_register_klaim = django_filters.CharFilter(field_name='register_klaim__nomor_register_klaim')
#     bupel_month = django_filters.NumberFilter(field_name='bupel', lookup_expr='month', widget=NumberInput(attrs={'min': 0, 'oninput':
#         "this.value =!!this.value && Math.abs(this.value) >= 0 ? Math.abs(this.value) : null", }))
#     bupel_year = django_filters.NumberFilter(field_name='bupel', lookup_expr='year', widget=NumberInput(attrs={'min': 0, 'oninput':
#         "this.value =!!this.value && Math.abs(this.value) >= 0 ? Math.abs(this.value) : null", }))
#     faskes = django_filters.ModelChoiceFilter(queryset=Faskes.objects.all(),
#                                               widget=autocomplete.ModelSelect2(
#                                                   url='verifikator:rumahsakit-autocomplete',
#                                               ))
#
#     class Meta:
#         model = SamplingDataKlaimCBG
#         fields = [
#
#             'JNSPEL',
#             'status',
#
#         ]
#
#     def __init__(self, *args, **kwargs):
#         request = kwargs.pop('request', None)  # Dapatkan 'request' dari kwargs
#         super().__init__(*args, **kwargs)
#
#         if request and request.user.is_authenticated:
#             # Filter queryset berdasarkan request.user jika pengguna terautentikasi
#             self.filters['faskes'].field.queryset = Faskes.objects.filter(kantor_cabang__in=request.user.kantorcabang_set.all())
