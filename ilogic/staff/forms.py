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


class DateInput(forms.DateInput):
    input_type = 'date'


class StatusRegisterKlaimForm(forms.ModelForm):
    status = forms.ChoiceField(choices=STATUS_CHOICES_TERIMA_REGISTER_STAFAK)

    class Meta:
        model = RegisterKlaim
        fields = ['status']


class PilihVerifikatorRegisterKlaimForm(forms.ModelForm):
    tgl_terima = forms.DateField(widget=DateInput)

    class Meta:
        model = RegisterKlaim
        fields = ['tgl_terima', 'no_ba_terima', 'verifikator']


class AlasanDikembalikanForm(forms.ModelForm):

    class Meta:
        model = RegisterKlaim
        fields = ['keterangan']


class IsActiveForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_active']
