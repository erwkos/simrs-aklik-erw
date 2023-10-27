from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.admin.widgets import FilteredSelectMultiple
from captcha.fields import CaptchaField
from requests import request

from faskes.models import KantorCabang, Faskes
from user.models import User


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    captcha = CaptchaField()


class CaptchaForm(forms.Form):
    captcha = CaptchaField()


class FormGroupChange(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all().exclude(name__in=('faskes', 'adminWEB')),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Group
        fields = ['groups']


class FormGroupNew(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all().exclude(name__in=('faskes', 'adminWEB')),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Group
        fields = '__all__'


class FormNewUser(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=False)
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all().exclude(name__in=('faskes', 'adminWEB')),
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


class FormNewFaskesUser(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=False)
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.filter(name='faskes'),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        initial=[u for u in Group.objects.filter(name='faskes')]
    )

    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'groups',
        ]


class AddUserFaskesForm(forms.ModelForm):
    faskes = forms.ModelMultipleChoiceField(queryset=Faskes.objects.all(),
                                            widget=forms.CheckboxSelectMultiple,
                                            required=True)

    class Meta:
        model = Faskes
        fields = ['faskes']


class IsActiveForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_active']


class IsStaffForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_staff']