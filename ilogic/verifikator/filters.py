import django_filters
from dal import autocomplete
from django.forms import NumberInput
from django_filters import OrderingFilter

from faskes.models import Faskes
from klaim.choices import JenisPelayananChoices
from klaim.models import DataKlaimCBG, DataKlaimObat, RegisterKlaim
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

KODE_JENIS_OBAT = (
    ('1', 'PRB'),
    ('2', 'Kronis'),
    ('3', 'Kemoterapi'),
)


class DataKlaimCBGFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=STATUS_CHOICES_VERIFIKATOR, label='Status')
    nomor_register_klaim = django_filters.CharFilter(field_name='register_klaim__nomor_register_klaim', label="No Reg")
    NOSEP = django_filters.CharFilter(field_name='NOSEP', label="No SEP")
    bupel_month = django_filters.NumberFilter(field_name='bupel', lookup_expr='month', widget=NumberInput(attrs={'min': 0, 'oninput':
        "this.value =!!this.value && Math.abs(this.value) >= 0 ? Math.abs(this.value) : null", }), label='Bulan Layan')
    bupel_year = django_filters.NumberFilter(field_name='bupel', lookup_expr='year', widget=NumberInput(attrs={'min': 0, 'oninput':
        "this.value =!!this.value && Math.abs(this.value) >= 0 ? Math.abs(this.value) : null", }), label='Tahun Layan')
    JNSPEL = django_filters.ChoiceFilter(choices=JenisPelayananChoices.choices, label="Jnspel")
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

    # class Meta:
    #     model = DataKlaimCBG
    #     fields = ['status', 'JNSPEL', 'NOSEP']


class DataKlaimObatFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=STATUS_CHOICES_VERIFIKATOR, label='Status')
    nomor_register_klaim = django_filters.CharFilter(field_name='register_klaim__nomor_register_klaim', label="No Reg")
    nosepapotek = django_filters.CharFilter(field_name='NoSEPApotek', label="No SEP Apotek")
    nosep = django_filters.CharFilter(field_name='NoSEPAsalResep', label="No SEP Asal")
    bupel_month = django_filters.NumberFilter(field_name='bupel', lookup_expr='month', widget=NumberInput(attrs={'min': 0, 'oninput':
        "this.value =!!this.value && Math.abs(this.value) >= 0 ? Math.abs(this.value) : null", }), label='Bulan Layan')
    bupel_year = django_filters.NumberFilter(field_name='bupel', lookup_expr='year', widget=NumberInput(attrs={'min': 0, 'oninput':
        "this.value =!!this.value && Math.abs(this.value) >= 0 ? Math.abs(this.value) : null", }), label='Tahun Layan')
    KdJenis = django_filters.ChoiceFilter(choices=KODE_JENIS_OBAT, label="Jenis Obat")
    nama_peserta = django_filters.CharFilter(field_name='NamaPeserta', label="Nama Peserta")

    o = OrderingFilter(
        fields=(
            ('status', 'Status'),
            ('faskes', 'RS'),
            ('register_klaim', 'NO REG'),
            ('KdJenis', 'Kode Jenis'),
            ('NoResep', 'No Resep'),
            ('TglResep', 'Tgl Resep'),
            ('bupel', 'Bulan Layan'),
            ('ByTagApt', 'By Tag Apt'),
            ('ByVerApt', 'By Ver Apt'),
            ('rufil', 'rufil'),
        )
    )


class DataKlaimCBGFaskesFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=STATUS_CHOICES_FASKES, label='Status')
    nomor_register_klaim = django_filters.CharFilter(field_name='register_klaim__nomor_register_klaim', label="No Reg")
    NOSEP = django_filters.CharFilter(field_name='NOSEP', label="No SEP")
    bupel_month = django_filters.NumberFilter(field_name='bupel', lookup_expr='month', widget=NumberInput(attrs={'min': 0, 'oninput':
        "this.value =!!this.value && Math.abs(this.value) >= 0 ? Math.abs(this.value) : null", }), label='Bulan Layan')
    bupel_year = django_filters.NumberFilter(field_name='bupel', lookup_expr='year', widget=NumberInput(attrs={'min': 0, 'oninput':
        "this.value =!!this.value && Math.abs(this.value) >= 0 ? Math.abs(this.value) : null", }), label='Tahun Layan')
    JNSPEL = django_filters.ChoiceFilter(choices=JenisPelayananChoices.choices, label="Jnspel")
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


class DataKlaimObatFaskesFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=STATUS_CHOICES_FASKES, label='Status')
    nomor_register_klaim = django_filters.CharFilter(field_name='register_klaim__nomor_register_klaim', label="No Reg")
    nosepapotek = django_filters.CharFilter(field_name='NoSEPApotek', label="No SEP Apotek")
    nosep = django_filters.CharFilter(field_name='NoSEPAsalResep', label="No SEP Asal")
    bupel_month = django_filters.NumberFilter(field_name='bupel', lookup_expr='month', widget=NumberInput(attrs={'min': 0, 'oninput':
        "this.value =!!this.value && Math.abs(this.value) >= 0 ? Math.abs(this.value) : null", }), label='Bulan Layan')
    bupel_year = django_filters.NumberFilter(field_name='bupel', lookup_expr='year', widget=NumberInput(attrs={'min': 0, 'oninput':
        "this.value =!!this.value && Math.abs(this.value) >= 0 ? Math.abs(this.value) : null", }), label='Tahun Layan')
    KdJenis = django_filters.ChoiceFilter(choices=KODE_JENIS_OBAT, label="Jenis Obat")
    nama_peserta = django_filters.CharFilter(field_name='NamaPeserta', label="Nama Peserta")

    o = OrderingFilter(
        fields=(
            ('status', 'Status'),
            ('register_klaim', 'NO REG'),
            ('KdJenis', 'Kode Jenis'),
            ('NoResep', 'No Resep'),
            ('TglResep', 'Tgl Resep'),
            ('bupel', 'Bulan Layan'),
            ('ByTagApt', 'By Tag Apt'),
        )
    )


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


class DownloadDataKlaimObatFilter(django_filters.FilterSet):
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
        model = DataKlaimObat
        fields = [
            'KdJenis',
            'status',
        ]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)  # Dapatkan 'request' dari kwargs
        super().__init__(*args, **kwargs)

        if request and request.user.is_authenticated:
            # Filter queryset berdasarkan request.user jika pengguna terautentikasi
            self.filters['faskes'].field.queryset = Faskes.objects.filter(kantor_cabang__in=request.user.kantorcabang_set.all())


class SinkronisasiVIBIVIDIFilter(django_filters.FilterSet):
    nomor_register_klaim = django_filters.CharFilter(field_name='register_klaim__nomor_register_klaim')
    status = django_filters.CharFilter(field_name='status')
    status_sinkron = django_filters.CharFilter(field_name='status_sinkron')
