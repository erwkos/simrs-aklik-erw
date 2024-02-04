import datetime

from django import forms
from django.contrib import messages
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


class DateInputMinMaxBAKB(forms.DateInput):
    input_type = 'date'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.attrs.setdefault('min', datetime.date.today())
        self.attrs.setdefault('max', datetime.date.today() + datetime.timedelta(days=9))


class DateInputMaxToday(forms.DateInput):
    input_type = 'date'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.setdefault('max', datetime.date.today())


class StatusRegisterKlaimForm(forms.ModelForm):
    status = forms.ChoiceField(choices=STATUS_CHOICES_TERIMA_REGISTER_VERIFIKATOR, initial=None)
    tgl_ba_lengkap = forms.DateField(widget=DateInputMinMaxBAKB)

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
    register = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}))
    file = forms.FileField(label='Upload File Excel', required=True,
                           help_text='Hanya menerima file dengan ekstensi `.xlsx` dan ukuran maksimal 2MB')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["register"].disabled = True

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file.name.split('.')[-1] != 'xlsx':
            raise ValidationError('Hanya menerima file dengan ekstensi `.xlsx`')
        elif file.size >= 1024 * 1024 * 2:
            raise ValidationError('File harus kurang dari 2MB')
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
    ket_pending_dispute= forms.CharField(required=False, min_length=5)

    class Meta:
        model = KeteranganPendingDispute
        fields = [
            'ket_pending_dispute',
        ]


class FinalisasiVerifikatorForm(forms.ModelForm):
    status = forms.ChoiceField(choices=STATUS_CHOICES_FINALISASI_REGISTER_VERIFIKATOR, initial=None)
    tgl_ba_verif = forms.DateField(widget=DateInputMaxToday, required=True)
    no_ba_hasil_verifikasi = forms.CharField(required=True, min_length=5)

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


class UploadDataKlaimForm(forms.Form):
    file = forms.FileField(label='Upload File Excel', required=True,
                           help_text='Hanya menerima file dengan ekstensi `.xlsx` dan ukuran maksimal 2MB')