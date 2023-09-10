from django import forms
from django.core.exceptions import ValidationError

from klaim.choices import StatusRegisterChoices, JenisPendingChoices
from klaim.models import (
    RegisterKlaim,
    DataKlaimCBG, KeteranganPendingDispute
)
from verifikator.models import HitungDataKlaim

STATUS_CHOICES_TERIMA_REGISTER_VERIFIKATOR = (
    ('Verifikasi', 'Verifikasi'),
)

STATUS_CHOICES_FINALISASI_REGISTER_VERIFIKATOR = (
    ('Selesai', 'Selesai'),
)

STATUS_CHOICES_DATA_KLAIM_VERIFIKATOR = (
    ('Layak', 'Layak'),
    ('Pending', 'Pending'),
    ('Dispute', 'Dispute'),
    ('Tidak Layak', 'Tidak Layak'),
)


class DateInput(forms.DateInput):
    input_type = 'date'

class StatusRegisterKlaimForm(forms.ModelForm):
    status = forms.ChoiceField(choices=STATUS_CHOICES_TERIMA_REGISTER_VERIFIKATOR, initial=None)

    class Meta:
        model = RegisterKlaim
        fields = [
            'tgl_ba_lengkap',
            'no_ba_lengkap',
            'status',
        ]

    # def clean_status(self):
    #     current_status = self.instance.status
    #     status = self.cleaned_data.get('status')
    #     if current_status != 'Terima':
    #         raise ValidationError('Hanya bisa menguhab status `Terima`.')
    #     return status


class ImportDataKlaimForm(forms.Form):
    register = forms.CharField(required=True, widget=forms.TextInput())
    file = forms.FileField()

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file.name.split('.')[-1] != 'xlsx':
            raise ValidationError('Hanya menerim file dengan ekstensi `.xlsx`')
        return file


class ImportUpdateDataKlaimCBGForm(forms.Form):
    register = forms.CharField(required=True, widget=forms.TextInput())
    file = forms.FileField()

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file.name.split('.')[-1] != 'xlsx':
            raise ValidationError('Hanya menerim file dengan ekstensi `.xlsx`')
        return file


class DataKlaimVerifikatorForm(forms.ModelForm):
    status = forms.ChoiceField(choices=STATUS_CHOICES_DATA_KLAIM_VERIFIKATOR)

    class Meta:
        model = DataKlaimCBG
        fields = [
            'status',
            'jenis_pending',
            'jenis_dispute',
        ]


class KeteranganPendingForm(forms.ModelForm):
    ket_pending_dispute= forms.CharField(required=False)

    class Meta:
        model = KeteranganPendingDispute
        fields = [
            'ket_pending_dispute',
        ]


class FinalisasiVerifikatorForm(forms.ModelForm):
    status = forms.ChoiceField(choices=STATUS_CHOICES_FINALISASI_REGISTER_VERIFIKATOR, initial=None)
    tgl_ba_verif = forms.DateField(widget=DateInput)

    class Meta:
        model = RegisterKlaim
        fields = [
            'tgl_ba_verif',
            'no_ba_hasil_verifikasi',
            'status',
        ]


class HitungDataKlaimForm(forms.ModelForm):

    class Meta:
        model = HitungDataKlaim
        fields = [
            'nomor_register_klaim',
            'jenis_klaim',
        ]
