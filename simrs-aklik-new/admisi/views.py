from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.hashers import make_password
from django.db import transaction

from django.views.generic import View, CreateView, DetailView
from pasien.models import Pasien, Pendaftaran, ResumeMedis
from user.models import User, UserRole
from poli.models import Poli, InvoicePoliPasien
from pasien.choices import (
    StatusPasienChoices,
    TipeLayanan,
    AgamaChoices,
    AsuransiChoices,
    RujukanChoices
)
from antrian.models import Antrian
from kasir.models import SummaryInvoice
from daerah.models import (
    Provinsi,
    Kabupaten,
    Kecamatan,
)


class PendaftarnRawatJalanPasienBaruView(DetailView, CreateView):
    queryset = Antrian.objects.all()
    template_name = 'admisi/pendaftaran-rawat-jalan.html'
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        antrian = self.get_object(self.get_queryset())
        context = {
            'antrian': antrian,
            'provinsi': Provinsi.objects.all(),
            'kabupaten': Kabupaten.objects.all(),
            'kecamatan': Kecamatan.objects.all(),
            'agama': AgamaChoices.choices,
            'asuransi': AsuransiChoices.choices,
            'rujukan': RujukanChoices.choices,
            'poli': Poli.objects.all(),
            'dokter': User.objects.filter(role__nama='dokter')
        }
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        antrian = self.get_object(self.get_queryset())
        data = request.POST
        pasien = Pasien.objects.create(
            nama=data.get('nama'),
            no_rekam_medis=Pasien.generate_no_rekam_medis(),
            nik=data.get('nik'),
            agama=data.get('agama'),
            jenis_kelamin=data.get('jenis_kelamin'),
            tanggal_lahir=data.get('tanggal_lahir'),
            provinsi=data.get('provinsi'),
            kabupaten=data.get('kabupaten'),
            kecamatan=data.get('kecamatan'),
            alamat=data.get('alamat'),
            status=StatusPasienChoices.BARU
        )
        poli = get_object_or_404(Poli, id=data.get('poli'))
        dokter = get_object_or_404(User, id=data.get('dokter'))
        resume_medis = ResumeMedis.objects.create(pasien=pasien, no_resume_medis=ResumeMedis.generate_no_rekam_medis())
        summary_invoice = SummaryInvoice.objects.create(
            kode_invoice=SummaryInvoice.generate_kode_invoice(),
            resume_medis=resume_medis,
            antrian=antrian
        )
        pendaftaran = Pendaftaran.objects.create(
            pasien=pasien,
            resume_medis=resume_medis,
            antrian=antrian,
            asuransi=data.get('asuransi'),
            no_peserta=data.get('no_peserta'),
            tipe_layanan=TipeLayanan.RAWAT_JALAN,
            poli=poli,
            dokter=dokter,
            biaya=27500,
            summary_invoice=summary_invoice,
            petugas=request.user
        )
        invoice_poli = InvoicePoliPasien.objects.create(
            resume_medis=resume_medis,
            summary_invoice=summary_invoice,
            total_harga=poli.harga,
            dokter=dokter,
            poli=poli
        )
        if pendaftaran.asuransi == AsuransiChoices.BPJS:
            pendaftaran.biaya = 0
            pendaftaran.save()
            invoice_poli.total_harga = 0
            invoice_poli.save()
        if pasien.account is None:
            user = User.objects.create(username=pendaftaran.pasien.no_rekam_medis,
                                       password=make_password(data.get('agama')))
            pasien.account = user
            pasien.save()
        antrian.task_id = 3
        antrian.save()
        return redirect('/admisi/antrian-admisi')


class PendaftarnRawatJalanPasienLamaView(CreateView):
    queryset = Antrian.objects.all()
    pk_url_kwarg = 'pk'

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = request.POST
        antrian = self.get_object(self.get_queryset())
        pasien = get_object_or_404(Pasien, id=data.get('pasien_id'))
        pasien.status = StatusPasienChoices.LAMA
        poli = get_object_or_404(Poli, id=data.get('poli'))
        dokter = get_object_or_404(User, id=data.get('dokter'))
        resume_medis = ResumeMedis.objects.create(pasien=pasien, no_resume_medis=ResumeMedis.generate_no_rekam_medis())
        summary_invoice = SummaryInvoice.objects.create(
            kode_invoice=SummaryInvoice.generate_kode_invoice(),
            resume_medis=resume_medis,
            antrian=antrian
        )
        pendaftaran = Pendaftaran.objects.create(
            pasien=pasien,
            resume_medis=resume_medis,
            antrian=antrian,
            asuransi=data.get('asuransi'),
            no_peserta=data.get('no_peserta'),
            tipe_layanan=TipeLayanan.RAWAT_JALAN,
            poli=poli,
            dokter=dokter,
            biaya=27500,
            summary_invoice=summary_invoice,
            petugas=request.user
        )
        invoice_poli = InvoicePoliPasien.objects.create(
            resume_medis=resume_medis,
            summary_invoice=summary_invoice,
            total_harga=poli.harga,
            dokter=dokter,
            poli=poli
        )
        if pendaftaran.asuransi == AsuransiChoices.BPJS:
            pendaftaran.biaya = 0
            pendaftaran.save()
            invoice_poli.total_harga = 0
            invoice_poli.save()
        antrian.task_id = 3
        antrian.save()
        return redirect('/admisi/antrian-admisi')



class PendaftarnRawatJalanPasienBaruDirectView(DetailView, CreateView):
    queryset = Antrian.objects.all()
    template_name = 'admisi/pendaftaran-rawat-jalan-direct.html'
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        antrian = self.get_object(self.get_queryset())
        context = {
            'antrian': antrian,
            'provinsi': Provinsi.objects.all(),
            'kabupaten': Kabupaten.objects.all(),
            'kecamatan': Kecamatan.objects.all(),
            'agama': AgamaChoices.choices,
            'asuransi': AsuransiChoices.choices,
            'rujukan': RujukanChoices.choices,
            'poli': Poli.objects.all(),
            'dokter': User.objects.filter(role__nama='dokter')
        }
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        antrian = self.get_object(self.get_queryset())
        data = request.POST
        pasien = Pasien.objects.create(
            nama=data.get('nama'),
            no_rekam_medis=Pasien.generate_no_rekam_medis(),
            nik=data.get('nik'),
            agama=data.get('agama'),
            jenis_kelamin=data.get('jenis_kelamin'),
            tanggal_lahir=data.get('tanggal_lahir'),
            provinsi=data.get('provinsi'),
            kabupaten=data.get('kabupaten'),
            kecamatan=data.get('kecamatan'),
            alamat=data.get('alamat'),
            status=StatusPasienChoices.BARU
        )
        poli = get_object_or_404(Poli, id=data.get('poli'))
        dokter = get_object_or_404(User, id=data.get('dokter'))
        resume_medis = ResumeMedis.objects.create(pasien=pasien, no_resume_medis=ResumeMedis.generate_no_rekam_medis())
        summary_invoice = SummaryInvoice.objects.create(
            kode_invoice=SummaryInvoice.generate_kode_invoice(),
            resume_medis=resume_medis,
            antrian=antrian
        )
        pendaftaran = Pendaftaran.objects.create(
            pasien=pasien,
            resume_medis=resume_medis,
            antrian=antrian,
            asuransi=data.get('asuransi'),
            no_peserta=data.get('no_peserta'),
            tipe_layanan=TipeLayanan.RAWAT_JALAN,
            poli=poli,
            dokter=dokter,
            biaya=27500,
            summary_invoice=summary_invoice,
            petugas=request.user
        )
        invoice_poli = InvoicePoliPasien.objects.create(
            resume_medis=resume_medis,
            summary_invoice=summary_invoice,
            total_harga=poli.harga,
            dokter=dokter,
            poli=poli
        )
        if pendaftaran.asuransi == AsuransiChoices.BPJS:
            pendaftaran.biaya = 0
            pendaftaran.save()
            invoice_poli.total_harga = 0
            invoice_poli.save()
        if pasien.account is None:
            user = User.objects.create(username=pendaftaran.pasien.no_rekam_medis,
                                       password=make_password(data.get('agama')))
            pasien.account = user
            pasien.save()
        antrian.task_id = 3
        antrian.save()
        return redirect('/admisi/antrian-admisi')


class PendaftarnRawatJalanPasienLamaDirectView(CreateView):
    queryset = Antrian.objects.all()
    pk_url_kwarg = 'pk'

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = request.POST
        antrian = self.get_object(self.get_queryset())
        pasien = get_object_or_404(Pasien, id=data.get('pasien_id'))
        pasien.status = StatusPasienChoices.LAMA
        poli = get_object_or_404(Poli, id=data.get('poli'))
        dokter = get_object_or_404(User, id=data.get('dokter'))
        resume_medis = ResumeMedis.objects.create(pasien=pasien, no_resume_medis=ResumeMedis.generate_no_rekam_medis())
        summary_invoice = SummaryInvoice.objects.create(
            kode_invoice=SummaryInvoice.generate_kode_invoice(),
            resume_medis=resume_medis,
            antrian=antrian
        )
        pendaftaran = Pendaftaran.objects.create(
            pasien=pasien,
            resume_medis=resume_medis,
            antrian=antrian,
            asuransi=data.get('asuransi'),
            no_peserta=data.get('no_peserta'),
            tipe_layanan=TipeLayanan.RAWAT_JALAN,
            poli=poli,
            dokter=dokter,
            biaya=27500,
            summary_invoice=summary_invoice,
            petugas=request.user
        )
        invoice_poli = InvoicePoliPasien.objects.create(
            resume_medis=resume_medis,
            summary_invoice=summary_invoice,
            total_harga=poli.harga,
            dokter=dokter,
            poli=poli
        )
        if pendaftaran.asuransi == AsuransiChoices.BPJS:
            pendaftaran.biaya = 0
            pendaftaran.save()
            invoice_poli.total_harga = 0
            invoice_poli.save()
        antrian.task_id = 3
        antrian.save()
        return redirect('/admisi/antrian-admisi')
