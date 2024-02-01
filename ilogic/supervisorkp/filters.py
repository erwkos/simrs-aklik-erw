import django_filters

from user.models import User


class UserSupervisorkpFilter(django_filters.FilterSet):

    class Meta:
        model = User
        fields = ['username',
                  'npp',
                  'first_name',
                  'last_name',
                  'groups__name',
                  ]