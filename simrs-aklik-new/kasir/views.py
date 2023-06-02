from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, UpdateView
from django.db import transaction

from .models import (
    SummaryInvoice
)
from .choices import (
    StatusPembayaranChoices,
    StatusLayananChoices
)
from antrian.models import Antrian
from pasien.models import Pendaftaran
from radiologi.models import LayananRadiologiPasien
from lab.models import LayananLabPasien
from poli.models import InvoicePoliPasien
from otherlayanan.models import (
    LayananEdukasiPasien,
    LayananTindakanPasien,
    LayananKonsultasiPasien,
    LayananMonitoringPasien
)
from farmasi.models import ObatPasien
from inventory.models import (
    AlatKesehatan,
    AlatKesehatanPasien
)


class AntrianKasirView(ListView):
    queryset = Pendaftaran.objects.filter(
        status_pembayaran=StatusPembayaranChoices.BELUM_BAYAR,
        status_layanan=StatusLayananChoices.SELESAI
    )
    template_name = 'kasir/antrian-kasir.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {
            'pendaftaran_list': self.get_queryset()
        }
        return context


class SumarryInvoiceView(DetailView):
    queryset = SummaryInvoice.objects.all()
    template_name = 'kasir/detail-invoice.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        obj = self.get_object(self.get_queryset())
        pendaftaran = Pendaftaran.objects.get(summary_invoice=obj)
        pasien = pendaftaran.pasien

        invoice_poli = InvoicePoliPasien.objects.get(summary_invoice=obj)
        invoice_poli_total = invoice_poli.total_harga

        invoice_radiologi = LayananRadiologiPasien.objects.filter(summary_invoice=obj)
        invoice_radiologi_total = sum([x.total_harga for x in invoice_radiologi])

        invoice_lab = LayananLabPasien.objects.filter(summary_invoice=obj)
        invoice_lab_total = sum([x.total_harga for x in invoice_lab])

        invoice_konsultasi = LayananKonsultasiPasien.objects.filter(summary_invoice=obj)
        invoice_konsultasi_total = sum([x.total_harga for x in invoice_konsultasi])

        invoice_tindakan = LayananTindakanPasien.objects.filter(summary_invoice=obj)
        invoice_tindakan_total = sum([x.total_harga for x in invoice_tindakan])

        invoice_monitoring = LayananMonitoringPasien.objects.filter(summary_invoice=obj)
        invoice_monitoring_total = sum([x.total_harga for x in invoice_monitoring])

        invoice_edukasi = LayananEdukasiPasien.objects.filter(summary_invoice=obj)
        invoice_edukasi_total = sum([x.total_harga for x in invoice_edukasi])

        invoice_obat = ObatPasien.objects.filter(summary_invoice=obj)
        invoice_obat_total = sum([x.total_harga for x in invoice_obat])

        invoice_alkes = AlatKesehatanPasien.objects.filter(summary_invoice=obj)
        invoice_alkes_total = sum([x.total_harga for x in invoice_alkes])

        totals = sum([
            pendaftaran.biaya,
            invoice_poli_total,
            invoice_radiologi_total,
            invoice_lab_total,
            invoice_konsultasi_total,
            invoice_tindakan_total,
            invoice_monitoring_total,
            invoice_edukasi_total,
            invoice_obat_total,
            invoice_alkes_total,
        ])
        obj.totals = totals
        obj.save()

        context = {
            'summary_invoice': obj,
            'pasien': pasien,
            'invoice_pendaftaran': pendaftaran,
            'invoice_poli': invoice_poli,
            'invoice_poli_total': invoice_poli_total,
            'invoice_radiologi': invoice_radiologi,
            'invoice_radiologi_total': invoice_radiologi_total,
            'invoice_lab': invoice_lab,
            'invoice_lab_total': invoice_lab_total,
            'invoice_konsultasi': invoice_konsultasi,
            'invoice_konsultasi_total': invoice_konsultasi_total,
            'invoice_tindakan': invoice_tindakan,
            'invoice_tindakan_total': invoice_tindakan_total,
            'invoice_monitoring': invoice_monitoring,
            'invoice_monitoring_total': invoice_monitoring_total,
            'invoice_edukasi': invoice_edukasi,
            'invoice_edukasi_total': invoice_edukasi_total,
            'invoice_obat': invoice_obat,
            'invoice_obat_total': invoice_obat_total,
            'invoice_alkes': invoice_alkes,
            'invoice_alkes_total': invoice_alkes_total,
            'totals': totals
        }
        return context


class KonfirmasiPembayaranRawatJalan(UpdateView):
    queryset = SummaryInvoice.objects.all()

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        obj = self.get_object(self.get_queryset())
        obj.status_pembayaran = StatusPembayaranChoices.SUDAH_BAYAR
        obj.petugas_kasir = request.user
        obj.save()
        antrian = Pendaftaran.objects.get(summary_invoice=obj).antrian
        antrian.task_id = 5
        antrian.save()
        for invoice_pendaftaran in Pendaftaran.objects.filter(summary_invoice=obj):
            invoice_pendaftaran.status_pembayaran = StatusPembayaranChoices.SUDAH_BAYAR
            invoice_pendaftaran.save()
        for invoice_poli in InvoicePoliPasien.objects.filter(summary_invoice=obj):
            invoice_poli.status_pembayaran = StatusPembayaranChoices.SUDAH_BAYAR
            invoice_poli.save()
        for invoice_radiologi in LayananRadiologiPasien.objects.filter(summary_invoice=obj):
            invoice_radiologi.status_pembayaran = StatusPembayaranChoices.SUDAH_BAYAR
            invoice_radiologi.save()
        for invoice_lab in LayananLabPasien.objects.filter(summary_invoice=obj):
            invoice_lab.status_pembayaran = StatusPembayaranChoices.SUDAH_BAYAR
            invoice_lab.save()
        for invoice_konsultasi in LayananKonsultasiPasien.objects.filter(summary_invoice=obj):
            invoice_konsultasi.status_pembayaran = StatusPembayaranChoices.SUDAH_BAYAR
            invoice_konsultasi.save()
        for invoice_tindakan in LayananTindakanPasien.objects.filter(summary_invoice=obj):
            invoice_tindakan.status_pembayaran = StatusPembayaranChoices.SUDAH_BAYAR
            invoice_tindakan.save()
        for invoice_monitoring in LayananMonitoringPasien.objects.filter(summary_invoice=obj):
            invoice_monitoring.status_pembayaran = StatusPembayaranChoices.SUDAH_BAYAR
            invoice_monitoring.save()
        for invoice_edukasi in LayananEdukasiPasien.objects.filter(summary_invoice=obj):
            invoice_edukasi.status_pembayaran = StatusPembayaranChoices.SUDAH_BAYAR
            invoice_edukasi.save()
        for invoice_obat in ObatPasien.objects.filter(summary_invoice=obj):
            invoice_obat.status_pembayaran = StatusPembayaranChoices.SUDAH_BAYAR
            invoice_obat.save()
        return redirect('/kasir/antrian-kasir')