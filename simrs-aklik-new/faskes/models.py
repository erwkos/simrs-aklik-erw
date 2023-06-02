from django.db import models


class Profil(models.Model):
    nama = models.CharField(max_length=255, null=True, blank=True)
    alamat = models.TextField(null=True, blank=True)
    logo = models.FileField(upload_to="logo/", null=True, blank=True)

    def __str__(self):
        return self.nama

    # def __str__(self):
    #     return f'{self.nama} {self.alamat}'
