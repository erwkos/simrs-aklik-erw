from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from user.models import User
from django import forms
from django.contrib.auth.models import Group


class CreateUserSupervisorkpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=False)
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all().exclude(name='faskes'),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'npp',
            'groups',
        ]


class EditUserSupervisorkpForm(UserChangeForm):

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=False)
    npp = forms.CharField(required=False)
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'npp',
            'groups',
            'is_staff',
            'is_active',
        ]




