import django_filters

from klaim.models import RegisterKlaim
from user.models import User
from django.contrib.auth.models import Group


class RegisterKlaimFaskesFilter(django_filters.FilterSet):
    class Meta:
        model = RegisterKlaim
        fields = ['jenis_klaim',
                  'status',
                  'verifikator',
                  ]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)  # Dapatkan 'request' dari kwargs
        super().__init__(*args, **kwargs)

        if request and request.user.is_authenticated:
            # Filter queryset berdasarkan request.user jika pengguna terautentikasi
            self.filters['verifikator'].field.queryset = User.objects.filter(kantorcabang__in=request.user.kantorcabang_set.all(),
                                                                             groups__in=Group.objects.filter(name='verifikator'))

class RegisterKlaimKhususFaskesFilter(django_filters.FilterSet):

    class Meta:
        model = RegisterKlaim
        fields = ['jenis_klaim',
                  'status',
                  ]
