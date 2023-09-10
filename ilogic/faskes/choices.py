from django.db import models
from django.utils.translation import gettext_lazy as _


class JenisFaskesChoices(models.TextChoices):
    FKTP = 'FKTP', _('FKTP')
    FKRTL = 'FKRTL', _('FKRTL')
