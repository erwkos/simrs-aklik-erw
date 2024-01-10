from django import forms
from django.core.exceptions import ValidationError
from django.forms import SelectDateWidget
from django.utils.translation import gettext_lazy as _

from klaim.models import (
    RegisterKlaim, DataKlaimCBG, JawabanPendingDispute, JenisKlaim, DataKlaimObat
)

import datetime

tahun_hari_ini = datetime.datetime.today().year

YEARS = [x for x in range(2016, tahun_hari_ini+1)]
YEARS.reverse()

STATUS_CHOICES_DATA_KLAIM_FASKES = (
    ('Pembahasan', 'Pembahasan'),
    ('Tidak Layak', 'Tidak Layak'),
)


class RegisterKlaimForm(forms.ModelForm):
    jenis_klaim = forms.ModelChoiceField(queryset=JenisKlaim.objects.all(), empty_label="Pilih Jenis Klaim")
    kasus_rawat_jalan_aju = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 0, 'oninput':
        "this.value =!!this.value && Math.abs(this.value) >= 0 ? Math.abs(this.value) : null", }))
    biaya_rawat_jalan_aju = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 0, 'oninput':
        "this.value =!!this.value && Math.abs(this.value) >= 0 ? Math.abs(this.value) : null"}))
    kasus_rawat_inap_aju = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 0, 'oninput':
        "this.value =!!this.value && Math.abs(this.value) >= 0 ? Math.abs(this.value) : null"}))
    biaya_rawat_inap_aju = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 0, 'oninput':
        "this.value =!!this.value && Math.abs(this.value) >= 0 ? Math.abs(this.value) : null"}))
    bulan_pelayanan = forms.DateField(widget=SelectDateWidget(years=YEARS))
    nomor_surat_pengajuan_rs = forms.CharField(min_length=5)

    class Meta:
        model = RegisterKlaim
        fields = [
            'jenis_klaim',
            'kasus_rawat_jalan_aju',
            'biaya_rawat_jalan_aju',
            'kasus_rawat_inap_aju',
            'biaya_rawat_inap_aju',
            'bulan_pelayanan',
            'nomor_surat_pengajuan_rs',
            # "is_pengajuan_ulang"
        ]
        # widgets = {
        #     'bulan_pelayanan': SelectDateWidget(years=YEARS)
        # }
        # # labels = {
        # #     "is_pengajuan_ulang": _("Pengajuan ulang pending/dispute")
        # # }
        # # help_texts = {
        # #     "is_pengajuan_ulang": _("Ceklis jika ini pengajuan ulang data klaim pending/dispute.")
        # # }


class UpdateRegisterKlaimForm(forms.ModelForm):
    class Meta:
        model = RegisterKlaim
        fields = [
            'jenis_klaim',
            'kasus_rawat_jalan_aju',
            'biaya_rawat_jalan_aju',
            'kasus_rawat_inap_aju',
            'biaya_rawat_inap_aju',
            'bulan_pelayanan',
            'nomor_surat_pengajuan_rs'
        ]
        widgets = {
            'bulan_pelayanan': SelectDateWidget(years=YEARS)
        }


class UpdateRegisterKlaimDisableForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["jenis_klaim"].disabled = True
        self.fields["kasus_rawat_jalan_aju"].disabled = True
        self.fields["biaya_rawat_jalan_aju"].disabled = True
        self.fields["kasus_rawat_inap_aju"].disabled = True
        self.fields["biaya_rawat_inap_aju"].disabled = True
        self.fields["bulan_pelayanan"].disabled = True
        self.fields["nomor_surat_pengajuan_rs"].disabled = True

    class Meta:
        model = RegisterKlaim
        fields = [
            'jenis_klaim',
            'kasus_rawat_jalan_aju',
            'biaya_rawat_jalan_aju',
            'kasus_rawat_inap_aju',
            'biaya_rawat_inap_aju',
            'bulan_pelayanan',
            'nomor_surat_pengajuan_rs'
        ]
        widgets = {
            'bulan_pelayanan': SelectDateWidget(years=YEARS)
        }


class DataKlaimCBGFaskesForm(forms.ModelForm):
    status = forms.ChoiceField(choices=STATUS_CHOICES_DATA_KLAIM_FASKES)

    class Meta:
        model = DataKlaimCBG
        fields = [
            'status',
        ]


class DataKlaimObatFaskesForm(forms.ModelForm):
    status = forms.ChoiceField(choices=STATUS_CHOICES_DATA_KLAIM_FASKES)

    class Meta:
        model = DataKlaimObat
        fields = [
            'status',
        ]


class JawabanPendingDisputeForm(forms.ModelForm):
    class Meta:
        model = JawabanPendingDispute
        fields = [
            'ket_jawaban_pending',
        ]
