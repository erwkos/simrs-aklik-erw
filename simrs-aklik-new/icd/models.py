from django.db import models


class ICD10(models.Model):
    nama = models.CharField(max_length=255)
    kode = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.nama} {self.kode}'


class ICD9(models.Model):
    nama = models.CharField(max_length=255)
    kode = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.nama} {self.kode}'
