import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.forms import DateInput, SelectDateWidget

from vpkaak.choices import StatusReviewChoices, StatusChoices
from vpkaak.models import RegisterPostKlaim, SamplingDataKlaimCBG

STATUS_REVIEW_CHOICES = [
    (StatusReviewChoices.Sesuai, StatusReviewChoices.Sesuai),
    (StatusReviewChoices.TidakSesuai, StatusReviewChoices.TidakSesuai),
]

STATUS_REGISTER_CHOICES_FINAL = [
    (StatusChoices.Finalisasi, StatusChoices.Finalisasi),
]

tahun_hari_ini = datetime.datetime.today().year

YEARS = [x for x in range(tahun_hari_ini - 1, tahun_hari_ini + 1)]
YEARS.reverse()


class DateInputMaxBA(forms.DateInput):
    input_type = 'date'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.attrs.setdefault('min', datetime.date.today())
        self.attrs.setdefault('max', datetime.date.today())


class RegisterPostKlaimForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['jenis_audit'].widget.attrs['onchange'] = 'toggleDiv()'

    # bulan_beban = forms.DateField(widget=SelectDateWidget(attrs={'type': 'month'}))
    bulan_beban = forms.DateField(widget=SelectDateWidget(years=YEARS))

    def clean_bulan_beban(self):
        bulan_beban = self.cleaned_data.get('bulan_beban')
        if bulan_beban:
            # Periksa apakah hanya bulan dan tahun yang diisi (tanpa tanggal)
            if bulan_beban.day is None:
                # Atur tanggal menjadi tanggal 1
                bulan_beban = bulan_beban.replace(day=1)
        return bulan_beban

    def clean(self):
        cleaned_data = super().clean()
        jenis_audit = cleaned_data.get('jenis_audit')
        if jenis_audit == 'AAK-FKRTL':
            if 'bulan_beban' in cleaned_data:
                del cleaned_data['bulan_beban']
        return cleaned_data

    class Meta:
        model = RegisterPostKlaim
        fields = [
            'jenis_audit',
            'inisiasi',
            'periode_awal',
            'periode_akhir',
            'surat_tugas',
            'bulan_beban',
            # 'nomor_BA_VPK_AAK',
            # 'staff_upk',
            # 'verifikator',
            # 'faskes',
            # 'kelas',
        ]
        widgets = {
            'periode_awal': DateInput(attrs={'type': 'date'}),
            'periode_akhir': DateInput(attrs={'type': 'date'}),
        }


class RegisterPostKlaimSupervisorKPForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['jenis_audit'].widget.attrs['onchange'] = 'toggleDiv()'

    # bulan_beban = forms.DateField(widget=SelectDateWidget(attrs={'type': 'year'}))
    bulan_beban = forms.DateField(widget=SelectDateWidget(years=YEARS))

    def clean_bulan_beban(self):
        bulan_beban = self.cleaned_data.get('bulan_beban')
        if bulan_beban:
            # Periksa apakah hanya bulan dan tahun yang diisi (tanpa tanggal)
            if bulan_beban.day is None:
                # Atur tanggal menjadi tanggal 1
                bulan_beban = bulan_beban.replace(day=1)
        return bulan_beban

    def clean(self):
        cleaned_data = super().clean()
        jenis_audit = cleaned_data.get('jenis_audit')
        if jenis_audit == 'AAK-FKRTL':
            if 'bulan_beban' in cleaned_data:
                del cleaned_data['bulan_beban']
        return cleaned_data

    class Meta:
        model = RegisterPostKlaim
        fields = [
            'jenis_audit',
            'inisiasi',
            'periode_awal',
            'periode_akhir',
            'surat_tugas',
            'bulan_beban',
            # 'nomor_BA_VPK_AAK',
            # 'staff_upk',
            # 'verifikator',
            # 'faskes',
            # 'kelas',
        ]
        widgets = {
            'periode_awal': DateInput(attrs={'type': 'date'}),
            'periode_akhir': DateInput(attrs={'type': 'date'}),
        }


class ImportSamplingDataKlaimForm(forms.Form):
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
        # elif file.size >= 1024 * 1024 * 2:
        #     raise ValidationError('File harus kurang dari 2MB')
        return file


class SamplingDataKlaimCBGForm(forms.ModelForm):
    status = forms.ChoiceField(choices=STATUS_REVIEW_CHOICES, label='Status')

    class Meta:
        model = SamplingDataKlaimCBG
        fields = [
            'status',
            'keterangan_review',
        ]


class FinalisasiRegisterPostKlaimForm(forms.ModelForm):
    status = forms.ChoiceField(choices=STATUS_REGISTER_CHOICES_FINAL, label='Status')

    class Meta:
        model = RegisterPostKlaim
        fields = [
            'status',
            # 'is_final',
        ]


class InputNomorBAForm(forms.ModelForm):
    tanggal_BA_VPK_AAK = forms.DateField(widget=DateInputMaxBA)

    class Meta:
        model = RegisterPostKlaim
        fields = ['nomor_BA_VPK_AAK', 'tanggal_BA_VPK_AAK', 'biaya_efisiensi']
