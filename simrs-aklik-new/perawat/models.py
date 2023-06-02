from django.db import models

from user.models import User
from poli.models import Poli


class DataPerawat(models.Model):
    account = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    poli = models.ForeignKey(Poli, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

