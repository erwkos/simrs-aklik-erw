from django.db import models

from user.models import User
from poli.models import Poli


class DataDokter(models.Model):
    account = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    sip = models.CharField(max_length=20, null=True, blank=True)  # Surat Izin Praktik
    poli = models.ForeignKey(Poli, on_delete=models.SET_NULL, blank=True, null=True)

