import datetime

from django import forms
from django.forms import SelectDateWidget

from klaim.models import (
    RegisterKlaim,
    JenisKlaim
)
from user.models import User

STATUS_CHOICES_TERIMA_REGISTER_STAFAK = (
    ('Terima', 'Terima'),
    ('Dikembalikan', 'Dikembalikan'),
)


class DateInputMaxToday(forms.DateInput):
    input_type = 'date'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.setdefault('max', datetime.date.today())


class StatusRegisterKlaimForm(forms.ModelForm):
    status = forms.ChoiceField(choices=STATUS_CHOICES_TERIMA_REGISTER_STAFAK)
    tgl_terima = forms.DateField(widget=DateInputMaxToday, required=False)
    no_ba_terima = forms.CharField(required=False, min_length=5)
    verifikator = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    keterangan = forms.CharField(min_length=5, required=False)

    class Meta:
        model = RegisterKlaim
        fields = ['status',
                  'tgl_terima',
                  'no_ba_terima',
                  'verifikator',
                  'keterangan']


class PilihVerifikatorRegisterKlaimForm(forms.ModelForm):
    tgl_terima = forms.DateField(widget=DateInputMaxToday, required=True)
    no_ba_terima = forms.CharField(required=True, min_length=5)
    verifikator = forms.ModelChoiceField(queryset=User.objects.all(), required=True)

    class Meta:
        model = RegisterKlaim
        fields = ['tgl_terima', 'no_ba_terima', 'verifikator']


class AlasanDikembalikanForm(forms.ModelForm):
    keterangan = forms.CharField(min_length=5, required=True)

    class Meta:
        model = RegisterKlaim
        fields = ['keterangan']


class IsActiveForm(forms.ModelForm):
    is_staff = forms.BooleanField(label="Verifikator Aktif", required=False,
                                  help_text="Jika Ter-Checklist, maka Verifikator masih bisa login dan "
                                            "melakukan verifikasi, namun tidak dapat menjadi PIC dan pembagian klaim.")

    class Meta:
        model = User
        fields = ['is_staff']


class ProsesBOAForm(forms.ModelForm):
    tgl_boa = forms.DateField(widget=DateInputMaxToday, required=True)
    class Meta:
        model = RegisterKlaim
        fields = ['tgl_boa']