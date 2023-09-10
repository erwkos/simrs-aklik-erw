from django.db import models

from user.models import User
import datetime


class HitungDataKlaim(models.Model):
    nomor_register_klaim = models.CharField(max_length=50, blank=True, null=True)
    tglhitung = models.DateField(blank=True, null=True)
    jamhitung = models.DateTimeField(blank=True, null=True)
    periodehitung = models.CharField(max_length=20, blank=True, null=True)
    jenis_klaim = models.CharField(max_length=50, blank=True, null=True)
    verifikator = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.jamhitung is None:
            self.jamhitung = datetime.datetime.now()
            self.tglhitung = self.jamhitung.date()
        if self.periodehitung is None:
            if 7 <= self.jamhitung.hour <= 12:
                self.periodehitung = '07 sd 12'
            elif 13 <= self.jamhitung.hour <= 17:
                self.periodehitung = '13 sd 17'
            elif 18 <= self.jamhitung.hour <= 20:
                self.periodehitung = '18 sd 20'
            elif 21 <= self.jamhitung.hour <= 23:
                self.periodehitung = '21 sd 23'
            elif self.jamhitung.hour == 24:
                self.periodehitung = '24'
            elif 0 <= self.jamhitung.hour <= 2:
                self.periodehitung = '00 sd 02'
            elif 3 <= self.jamhitung.hour <= 6:
                self.periodehitung = '03 sd 06'
        super(HitungDataKlaim, self).save(*args, **kwargs)

