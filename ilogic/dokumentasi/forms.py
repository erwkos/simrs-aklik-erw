from django import forms

from dokumentasi.models import PolaRules


class PolaRulesForm(forms.ModelForm):
    class Meta:
        model = PolaRules
        field = '__all__'
        exclude = []


class AddPolaRulesForm(forms.ModelForm):
    class Meta:
        model = PolaRules
        field = '__all__'
        exclude = [
            'nama_rules',
            'diagnosis_utama',
            'diagnosis_sekunder',
            'is_aju',
            'dt_is_aju',
            'is_approved_asdep',
            'dt_is_approved_asdep',
            'is_approved_depdirbid',
            'dt_is_approved_depdirbid'
        ]
