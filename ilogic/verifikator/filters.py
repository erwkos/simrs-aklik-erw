import django_filters
from dal import autocomplete
from django.forms import NumberInput
from django_filters import OrderingFilter

from faskes.models import Faskes
from klaim.models import DataKlaimCBG
from user.models import User
from django.contrib.auth.models import Group

STATUS_CHOICES_VERIFIKATOR = (
    ('Proses', 'Proses'),
    ('Layak', 'Layak'),
    ('Pending', 'Pending'),
    ('Dispute', 'Dispute'),
    ('Tidak Layak', 'Tidak Layak'),
)

STATUS_CHOICES_FASKES = (
    ('Pending', 'Pending'),
    ('Dispute', 'Dispute'),
    ('Tidak Layak', 'Tidak Layak'),
    ('Pembahasan', 'Pembahasan'),
)


class DataKlaimCBGFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=STATUS_CHOICES_VERIFIKATOR)
    nomor_register_klaim = django_filters.CharFilter(field_name='register_klaim__nomor_register_klaim', label="Nomor Register")
    bupel_month = django_filters.NumberFilter(field_name='bupel', lookup_expr='month', widget=NumberInput(attrs={'min': 0, 'oninput':
        "this.value =!!this.value && Math.abs(this.value) >= 0 ? Math.abs(this.value) : null", }), label='Bulan Layan')
    bupel_year = django_filters.NumberFilter(field_name='bupel', lookup_expr='year', widget=NumberInput(attrs={'min': 0, 'oninput':
        "this.value =!!this.value && Math.abs(this.value) >= 0 ? Math.abs(this.value) : null", }), label='Tahun Layan')
    nama_peserta = django_filters.CharFilter(field_name='NMPESERTA', label="Nama Peserta")

    o = OrderingFilter(
        fields=(
            ('status', 'Status'),
            ('faskes', 'RS'),
            ('register_klaim', 'NO REG'),
            ('NOSEP', 'No SEP'),
            ('TGLSEP', 'In'),
            ('TGLPULANG', 'Out'),
            ('JNSPEL', 'JNS PEL'),
            ('NOKARTU', 'Noka'),
            ('NMPESERTA', 'Nama'),
            ('bupel', 'Bulan Layan'),
            ('POLI', 'POLI'),
            ('KDINACBG', 'CBG'),
            ('BYPENGAJUAN', 'Biaya'),
        )
    )

    class Meta:
        model = DataKlaimCBG
        fields = ['JNSPEL', 'status', 'NOSEP']


class DataKlaimCBGFaskesFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=STATUS_CHOICES_FASKES)
    # nomor_register_klaim = django_filters.CharFilter(field_name='register_klaim__nomor_register_klaim')
    bupel_month = django_filters.NumberFilter(field_name='bupel', lookup_expr='month', widget=NumberInput(attrs={'min': 0, 'oninput':
        "this.value =!!this.value && Math.abs(this.value) >= 0 ? Math.abs(this.value) : null", }))
    bupel_year = django_filters.NumberFilter(field_name='bupel', lookup_expr='year', widget=NumberInput(attrs={'min': 0, 'oninput':
        "this.value =!!this.value && Math.abs(this.value) >= 0 ? Math.abs(this.value) : null", }))


    class Meta:
        model = DataKlaimCBG
        fields = ['JNSPEL', 'status']


class DownloadDataKlaimCBGFilter(django_filters.FilterSet):
    nomor_register_klaim = django_filters.CharFilter(field_name='register_klaim__nomor_register_klaim')
    bupel_month = django_filters.NumberFilter(field_name='bupel', lookup_expr='month', widget=NumberInput(attrs={'min': 0, 'oninput':
        "this.value =!!this.value && Math.abs(this.value) >= 0 ? Math.abs(this.value) : null", }))
    bupel_year = django_filters.NumberFilter(field_name='bupel', lookup_expr='year', widget=NumberInput(attrs={'min': 0, 'oninput':
        "this.value =!!this.value && Math.abs(this.value) >= 0 ? Math.abs(this.value) : null", }))
    faskes = django_filters.ModelChoiceFilter(queryset=Faskes.objects.all(),
                                              widget=autocomplete.ModelSelect2(
                                                  url='verifikator:rumahsakit-autocomplete',
                                              ))

    class Meta:
        model = DataKlaimCBG
        fields = [
            # 'nomor_register_klaim',
            # 'bupel',
            'JNSPEL',
            'status',
            # 'faskes',
            # 'verifikator',
        ]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)  # Dapatkan 'request' dari kwargs
        super().__init__(*args, **kwargs)

        if request and request.user.is_authenticated:
            # Filter queryset berdasarkan request.user jika pengguna terautentikasi
            self.filters['faskes'].field.queryset = Faskes.objects.filter(kantor_cabang__in=request.user.kantorcabang_set.all())
