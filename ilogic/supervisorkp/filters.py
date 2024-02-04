import django_filters
from django.contrib.auth.models import Group
from django import forms

from user.models import User


class UserSupervisorkpFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    npp = django_filters.CharFilter(lookup_expr='icontains')
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    groups__name = django_filters.ModelMultipleChoiceFilter(queryset=Group.objects.all(),
                                                            widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = User
        fields = ['username',
                  'npp',
                  'first_name',
                  'last_name',
                  'groups__name',
                  ]