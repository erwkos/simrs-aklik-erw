from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime
import pytz


class User(AbstractUser):
    email = models.EmailField(blank=True, null=True) # unique dioff saja, ternyata error saat pembuatan
    meta = models.CharField(max_length=255, null=True, blank=True)

    npp = models.CharField(max_length=25, default="NPP Kosong")

    login_attempt = models.IntegerField(default=0)
    blocked_count = models.IntegerField(default=0)
    block_login_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.username}'

    def check_permissions(self, group_list):
        group_list_obj = Group.objects.filter(name__in=group_list)
        if len(group_list) != group_list_obj.count():
            groups = [g for g in group_list if g not in [g.name for g in group_list_obj]]
            raise ValueError(f'Group belum di inisiasi!!!, {groups}')
        return all(group in self.groups.all() for group in group_list_obj)

    def login_is_blocked(self):
        if self.block_login_time is not None:
            return bool(self.block_login_time > datetime.now(pytz.timezone(settings.TIME_ZONE)))
        return False


# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     user_agent = models.CharField(max_length=255, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

