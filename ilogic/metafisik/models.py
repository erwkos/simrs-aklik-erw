from django.db import models


class NoBAMetafisik(models.Model):
    no_surat_bast = models.CharField(max_length=50, null=True, blank=True, unique=True)
    tgl_bast = models.DateField(null=True, blank=True)
    tgl_pelayanan = models.DateField(null=True, blank=True)
    kdkrlayan = models.CharField(max_length=10, null=True, blank=True)
    kdkclayan = models.CharField(max_length=10, null=True, blank=True)
    kdppklayan = models.CharField(max_length=20, null=True, blank=True)
    nmppklayan = models.CharField(max_length=255, null=True, blank=True)
    total_klaim = models.IntegerField(null=True, blank=True)
    total_redflag = models.IntegerField(null=True, blank=True)
    total_layak = models.IntegerField(null=True, blank=True)
    total_pending = models.IntegerField(null=True, blank=True)
    total_tidaklayak = models.IntegerField(null=True, blank=True)
    is_import = models.BooleanField(default=False)
    is_bagi = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.no_surat_bast} - {self.tgl_bast}"

    def update_total_redflag(self):
        self.total_redflag = DataKlaimCBGMetafisik.objects.filter(no_bast=self).count()
        self.save()


# Create your models here.
class DataKlaimCBGMetafisik(models.Model):
    no_bast = models.ForeignKey(NoBAMetafisik, on_delete=models.CASCADE, null=True)
    nokapst = models.CharField(max_length=50, null=True, blank=True)
    tgldtgsep = models.DateField(null=True, blank=True)
    tglplgsep = models.DateField(null=True, blank=True)
    nosjp = models.CharField(max_length=50, null=True, blank=True)
    nmtkp = models.CharField(max_length=255, null=True, blank=True)
    kdinacbgs = models.CharField(max_length=10, null=True, blank=True)
    nminacbgs = models.CharField(max_length=255, null=True, blank=True)
    kddiagprimer = models.CharField(max_length=255, null=True, blank=True)
    nmdiagprimer = models.CharField(max_length=255, null=True, blank=True)
    diagsekunder = models.CharField(max_length=3000, null=True, blank=True)
    prosedur = models.CharField(max_length=3000, null=True, blank=True)
    klsrawat = models.CharField(max_length=10, null=True, blank=True)
    nmjnspulang = models.CharField(max_length=50, null=True, blank=True)
    politujsep = models.CharField(max_length=10, null=True, blank=True)
    kddokter = models.CharField(max_length=10, null=True, blank=True)
    nmdokter = models.CharField(max_length=255, null=True, blank=True)
    umur_tahun = models.IntegerField(null=True, blank=True)
    kdsa = models.CharField(max_length=50, null=True, blank=True)
    kdsd = models.CharField(max_length=50, null=True, blank=True)
    deskripsisd = models.CharField(max_length=50, null=True, blank=True)
    kdsi = models.CharField(max_length=50, null=True, blank=True)
    kdsp = models.CharField(max_length=50, null=True, blank=True)
    deskripsisp = models.CharField(max_length=50, null=True, blank=True)
    kdsr = models.CharField(max_length=50, null=True, blank=True)
    deskripsisr = models.CharField(max_length=50, null=True, blank=True)
    tarifsa = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    tarifsd = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    tarifsi = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    tarifsp = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    tarifsr = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    bytagsep = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    tarifgrup = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    biayars = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # redflag, deskripsi, dan indikator
    id_logik = models.CharField(max_length=100, null=True, blank=True)
    redflag = models.CharField(max_length=1000, null=True, blank=True)
    deskripsi_redflag = models.CharField(max_length=2000, null=True, blank=True)
    keterangan_aksi = models.CharField(max_length=2000, null=True, blank=True)
    indikator = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.no_bast} - {self.nosjp}'
