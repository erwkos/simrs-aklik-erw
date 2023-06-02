from django.db import models
from django.utils.translation import gettext_lazy as _


class GenderChoices(models.TextChoices):
    PRIA = 'Pria', _('Pria')
    WANITA = 'Wanita', _('Wanita')


