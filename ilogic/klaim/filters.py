import django_filters

from klaim.models import RegisterKlaim
from user.models import User
from django.contrib.auth.models import Group


class RegisterKlaimFaskesFilter(django_filters.FilterSet):
    verifikator = django_filters.ModelChoiceFilter(queryset=User.objects.filter(groups__in=Group.objects.filter(name='verifikator')))

    class Meta:
        model = RegisterKlaim
        fields = ['jenis_klaim',
                  'status',
                  # 'verifikator',
                  ]
