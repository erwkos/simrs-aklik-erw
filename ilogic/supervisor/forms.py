from django import forms

from klaim.models import RegisterKlaim
from user.models import User


class PilihVerifikatorRegisterKlaimSupervisorForm(forms.ModelForm):

    class Meta:
        model = RegisterKlaim
        fields = ['verifikator']
