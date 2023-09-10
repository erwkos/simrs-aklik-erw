
from collections import Counter
import random

from klaim.choices import (
    JenisPelayananChoices,
    StatusDataKlaimChoices
)
from klaim.models import DataKlaimCBG


def pembagian_tugas(queryset_id, verifikator):
    print(queryset_id)
    DataKlaimCBG.objects.filter(id__in=queryset_id).update(status='Proses', prosespending=False, prosesdispute=False, prosesklaim=False)
    queryset_dataklaim = DataKlaimCBG.objects.filter(id__in=queryset_id)
    print('pembagian tugas:', queryset_dataklaim)

    NMPESERTA_RJ = [obj.NMPESERTA for obj in queryset_dataklaim.filter(
        JNSPEL=JenisPelayananChoices.RAWAT_JALAN)]
    list_nmpeserta_sort_freq = [item for items, c in Counter(NMPESERTA_RJ).most_common() for item in [items] * c]
    list_nmpeserta_no_duplicate = list(dict.fromkeys(list_nmpeserta_sort_freq))

    index = random.randrange(verifikator.count())
    for i in range(len(list_nmpeserta_no_duplicate)):
        queryset_dataklaim.filter(NMPESERTA=list_nmpeserta_no_duplicate[i], JNSPEL=JenisPelayananChoices.RAWAT_JALAN). \
            update(verifikator=verifikator[index], status=StatusDataKlaimChoices.PROSES)
        if index == verifikator.count() - 1:
            index = 0
        else:
            index += 1
    print('11111')

    index = random.randrange(verifikator.count())
    for obj in queryset_dataklaim.filter(JNSPEL=JenisPelayananChoices.RAWAT_INAP):
        obj.verifikator = verifikator[index]
        obj.status = StatusDataKlaimChoices.PROSES
        obj.save()
        if index == verifikator.count() - 1:
            index = 0
        else:
            index += 1
    print('2222')

