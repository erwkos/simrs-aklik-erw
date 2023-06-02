from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusGeneralisChoices(models.TextChoices):
    NORMAL = 'Normal', _('Normal')
    ABNORMAL = 'Abnornal', _('Abnormal')


class KesadaranChoices(models.TextChoices):
    COMPOS_MENTIS = 'Compos Mentis', _('Compos Mentis')
    APATIS = 'Apatis', _('Apatis')
    SOMNOLEN = 'Somnolen', _('Somnolen')
    SOPOR = 'Sopor', _('Sopor')
    COMA = 'Coma', _('Coma')


class KondisiUmumChoices(models.TextChoices):
    BAIK = 'Baik', _('Baik')
    BURUK = 'Buruk', _('Buruk')
    SEDANG = 'Sedang', _('Sedang')
