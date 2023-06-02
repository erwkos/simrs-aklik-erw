from django.db import models


class Gizi(models.Model):
    nama = models.CharField(max_length=100)
    harga = models.FloatField(default=0)
    stok = models.IntegerField()
