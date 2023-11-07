from django import forms

from klaim.choices import NamaJenisKlaimChoices
from klaim.models import RegisterKlaim, SLA, JenisKlaim
from user.models import User


class PilihVerifikatorRegisterKlaimSupervisorForm(forms.ModelForm):

    class Meta:
        model = RegisterKlaim
        fields = ['verifikator']


class IsActiveForm(forms.ModelForm):
    is_staff = forms.BooleanField(label="Verifikator Aktif", required=False,
                                  help_text="Jika Ter-Checklist, maka Verifikator masih bisa login dan "
                                            "melakukan verifikasi, namun tidak dapat menjadi PIC dan pembagian klaim.")
    is_active = forms.BooleanField(label="Bisa Login", required=False,
                                   help_text="Jika Ter-Checklist, maka Verifikator tidak login sama sekali.")

    class Meta:
        model = User
        fields = ['is_staff', 'is_active']


class SLACreateForm(forms.ModelForm):
    jenis_klaim = forms.ModelChoiceField(queryset=JenisKlaim.objects.all(),
                                         help_text="Hanya bisa ditambah untuk satu jenis klaim saja")
    plus_hari_sla = forms.IntegerField(label="Jumlah Hari", help_text="Pilih Range Hari 1-9, "
                                                                      "misalnya Jumlah Hari yang disetting adalah 2, "
                                                                      "maka SLA Verifikasi adalah "
                                                                      "Tgl BA Lengkap + 2 hari",
                                       widget=forms.NumberInput(attrs={'min': 1, 'max': 9, 'oninput':
                                           "this.value =!!this.value && Math.abs(this.value) >= 1 && Math.abs(this.value) <= 9? Math.abs(this.value) : null"})
                                       )

    class Meta:
        model = SLA
        fields = ['jenis_klaim',
                  'plus_hari_sla',
                  ]


class SLAUpdateForm(forms.ModelForm):
    plus_hari_sla = forms.IntegerField(label="Jumlah Hari", help_text="Pilih Range Hari 1-9, "
                                                                      "misalnya Jumlah Hari yang disetting adalah 2, "
                                                                      "maka SLA Verifikasi adalah "
                                                                      "Tgl BA Lengkap + 2 hari",
                                       widget=forms.NumberInput(attrs={'min': 1, 'max': 9, 'oninput':
                                           "this.value =!!this.value && Math.abs(this.value) >= 1 && Math.abs(this.value) <= 9? Math.abs(this.value) : null"})
                                       )

    class Meta:
        model = SLA
        fields = ['plus_hari_sla']
