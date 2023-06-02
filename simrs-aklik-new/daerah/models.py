from django.db import models


class Provinsi(models.Model):
    nama = models.CharField(max_length=100)


class Kabupaten(models.Model):
    nama = models.CharField(max_length=100)


class Kecamatan(models.Model):
    nama = models.CharField(max_length=100)


class Daerah(models.Model):
    nama = models.CharField(max_length=100)

