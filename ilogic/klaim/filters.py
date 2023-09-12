import django_filters

from klaim.models import RegisterKlaim
from user.models import User
from django.contrib.auth.models import Group


# def verifikator_kantor_cabang(request):
#     queryset = User.objects.filter(kantorcabang=request.user.kantorcabang_set.all().first())
#     # queryset = User.objects.filter(groups__in=Group.objects.filter(name='verifikator'),
#     #                                kantorcabang=request.user.kantorcabang_set.first())
#     return queryset
#

class RegisterKlaimFaskesFilter(django_filters.FilterSet):
    # def __init__(self, data=None, queryset=None, *, request=None, user=None, prefix=None):
    #     super().__init__(data=data, queryset=queryset, prefix=prefix)
    #     self.filters['verifikator'].queryset = User.objects.filter(groups__in=Group.objects.filter(name='verifikator'))
    #
    verifikator = django_filters.ModelChoiceFilter(queryset=User.objects.filter(groups__in=Group.objects.filter(name='verifikator')))
    class Meta:
        model = RegisterKlaim
        fields = ['jenis_klaim',
                  'status',
                  # 'verifikator',
                  ]


class RegisterKlaimKhususFaskesFilter(django_filters.FilterSet):

    class Meta:
        model = RegisterKlaim
        fields = ['jenis_klaim',
                  'status',
                  ]
