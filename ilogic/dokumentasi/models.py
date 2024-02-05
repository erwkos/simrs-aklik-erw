from django.core.validators import MinValueValidator
from django.db import models


class ICD10(models.Model):
    kode = models.CharField(max_length=250)
    nama = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.kode} - {self.nama}'


class ProgressVersion(models.Model):
    version = models.IntegerField(unique=True)

    is_aju = models.BooleanField(default=False)
    dt_is_aju = models.DateTimeField(blank=True, null=True)

    is_approved_asdep = models.BooleanField(default=False)
    dt_is_approved_asdep = models.DateTimeField(blank=True, null=True)

    is_approved_depdirbid = models.BooleanField(default=False)
    dt_is_approved_depdirbid = models.DateTimeField(blank=True, null=True)

    open_edit = models.BooleanField(default=False)
    dt_open_edit = models.DateTimeField(blank=True, null=True)

    is_rejected = models.BooleanField(default=False)
    dt_is_rejected = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.version}'


# Create your models here.
class PolaRules(models.Model):
    progress_version = models.ForeignKey(ProgressVersion, on_delete=models.CASCADE, blank=True, null=True)
    nama_rules = models.CharField(max_length=250)
    diagnosis_utama = models.CharField(max_length=250, blank=True, null=True)
    diagnosis_sekunder = models.CharField(max_length=250, blank=True, null=True)
    prosedur = models.CharField(max_length=250, blank=True, null=True)
    jenis_pelayanan = models.CharField(max_length=250, blank=True, null=True)
    cmg = models.CharField(max_length=250, blank=True, null=True)
    los = models.IntegerField(blank=True, null=True)
    cbg = models.CharField(max_length=250, blank=True, null=True)
    severity_level = models.CharField(max_length=250, blank=True, null=True)
    jenis_kelamin = models.CharField(max_length=250, blank=True, null=True)
    usia = models.IntegerField(blank=True, null=True)
    pesan = models.TextField()
    models_polarules = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.nama_rules}'
