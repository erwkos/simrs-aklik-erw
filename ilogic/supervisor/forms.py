from django import forms

from klaim.models import RegisterKlaim
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
