import django_filters
from dal import autocomplete
from django.forms import NumberInput, DateInput
from django import forms
from django.utils import timezone

from faskes.models import Faskes
from metafisik.models import NoBAMetafisik


class MonthYearInput(forms.DateInput):
    input_type = 'month'


class ListBAFilter(django_filters.FilterSet):
    no_surat_bast = django_filters.CharFilter(field_name='no_surat_bast', lookup_expr='icontains', label='No Surat BPK')
    tgl_bast = django_filters.DateFilter(field_name='tgl_bast', widget=DateInput(attrs={'type': 'date'}), label='Tanggal BPK')
    # Dropdown untuk bulan (1-12)
    MONTH_CHOICES = [(i, i) for i in range(1, 13)]
    bupel_month = django_filters.ChoiceFilter(field_name='tgl_pelayanan', lookup_expr='month', choices=MONTH_CHOICES, label='Bulan Layan')

    # Dropdown untuk tahun (misalnya dari 2000 hingga tahun sekarang)
    current_year = timezone.now().year
    YEAR_CHOICES = [(year, year) for year in range(2024, current_year + 1)]
    bupel_year = django_filters.ChoiceFilter(field_name='tgl_pelayanan', lookup_expr='year', choices=YEAR_CHOICES,
                                             label='Tahun Layan')
    nmppklayan = django_filters.ModelChoiceFilter(field_name='nmppklayan',
                                                  queryset=Faskes.objects.all(),
                                                  widget=autocomplete.ModelSelect2(url='verifikator:rumahsakit-autocomplete'),
                                                  label='Rumah Sakit')
    is_import = django_filters.BooleanFilter(field_name='is_import', label='Import')
    is_bagi = django_filters.BooleanFilter(field_name='is_bagi', label='Bagi')

    class Meta:
        model = NoBAMetafisik
        fields = ['no_surat_bast', 'tgl_bast', 'bupel_month', 'bupel_year', 'nmppklayan', 'is_import', 'is_bagi']



