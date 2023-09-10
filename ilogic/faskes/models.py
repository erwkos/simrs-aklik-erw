from django.db import models

from user.models import User
from .choices import (
    JenisFaskesChoices
)


class Kepwil(models.Model): #kepwil
    nama = models.CharField(max_length=100, unique=True)
    kode_kepil = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f'{self.nama}'


class KantorCabang(models.Model):
    nama = models.CharField(max_length=100, unique=True)
    kode_cabang = models.CharField(max_length=30, unique=True)
    kepwil = models.ForeignKey(Kepwil, on_delete=models.CASCADE) #kepwil
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f'{self.nama}'


class Faskes(models.Model):
    nama = models.CharField(max_length=250)
    kode_ppk = models.CharField(max_length=100, unique=True)
    jenis = models.CharField(max_length=50,
                             choices=JenisFaskesChoices.choices, blank=True, null=True)

    kantor_cabang = models.ForeignKey(KantorCabang, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f'{self.nama}'
