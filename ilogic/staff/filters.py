import django_filters

from faskes.models import Faskes
from klaim.models import DataKlaimCBG
from dal import autocomplete

STATUS_CHOICES_VERIFIKATOR = (
    ('Proses', 'Proses'),
    ('Layak', 'Layak'),
    ('Pending', 'Pending'),
    ('Dispute', 'Dispute'),
    ('Tidak Layak', 'Tidak Layak'),
)


class DataKlaimAmbilNoSepFilter(django_filters.FilterSet):
    nomor_register_klaim = django_filters.CharFilter(field_name='register_klaim__nomor_register_klaim', label="No Reg")
    status = django_filters.ChoiceFilter(choices=STATUS_CHOICES_VERIFIKATOR)
