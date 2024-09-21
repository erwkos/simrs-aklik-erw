import datetime
import random
from collections import Counter
from datetime import timedelta

import xlsxwriter
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse

from klaim.choices import StatusDataKlaimChoices, JenisPelayananChoices
from klaim.models import RegisterKlaim, DataKlaimCBG, SLA
from metafisik.models import DataKlaimCBGMetafisik, NoBAMetafisik
from user.models import User


def export_data_klaim(no_bast_export):
    """
    Fungsi untuk mengekspor data klaim ke file Excel.
    """
    queryset_dataklaim_cbg_metafisik = DataKlaimCBGMetafisik.objects.filter(no_bast__no_surat_bast=no_bast_export)
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename={date}-samplingmetafisik.xlsx'.format(
        date=datetime.datetime.now().strftime('%Y-%m-%d'),
    )
    workbook = xlsxwriter.Workbook(response, {'in_memory': True})
    worksheet = workbook.add_worksheet('Sampling Metafisik')

    # Define the titles for columns
    columns = [
        'no_surat_bast',
        'tgl_bast',
        'nokapst',
        'nosjp',
        'tgldtgsjp',
        'tglplgsjp',
        'tgl_pelayanan',
        'kdppklayan',
        'nmppklayan',
        'nmtkp',
        'kdinacbgs',
        'nminacbgs',
        'kddiagprimer',
        'nmdiagprimer',
        'diagsekunder',
        'prosedur',
        'klsrawat',
        'nmjnspulang',
        'kddokter',
        'nmdokter',
        'umur_tahun',
        'kdsa',
        'kdsd',
        'deskripsid',
        'kdsi',
        'kdsp',
        'deskripsisp',
        'kdsr',
        'deskripsisr',
        'tarifsa',
        'tarifsd',
        'tarifsi',
        'tarifsp',
        'tarifsr',
        'tarifgrup',
        'bytagsep',
        'id_logik',
        'redflag',
        'deskripsi_redflag',
        'keterangan_aksi',
    ]

    # Assign the titles for each cell of the header
    for col_num, column_title in enumerate(columns):
        worksheet.write(0, col_num, column_title)

    # Iterate through all
    date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})
    for row_num, dataklaim in enumerate(queryset_dataklaim_cbg_metafisik, start=1):
        row = [
            dataklaim.no_bast.no_surat_bast,
            dataklaim.no_bast.tgl_bast,
            dataklaim.nokapst,
            dataklaim.nosjp,
            dataklaim.tgldtgsep,
            dataklaim.tglplgsep,
            dataklaim.no_bast.tgl_pelayanan,
            dataklaim.no_bast.kdppklayan,
            dataklaim.no_bast.nmppklayan,
            dataklaim.nmtkp,
            dataklaim.kdinacbgs,
            dataklaim.nminacbgs,
            dataklaim.kddiagprimer,
            dataklaim.nmdiagprimer,
            dataklaim.diagsekunder,
            dataklaim.prosedur,
            dataklaim.klsrawat,
            dataklaim.nmjnspulang,
            dataklaim.kddokter,
            dataklaim.nmdokter,
            dataklaim.umur_tahun,
            dataklaim.kdsa,
            dataklaim.kdsd,
            dataklaim.deskripsisd,
            dataklaim.kdsi,
            dataklaim.kdsp,
            dataklaim.deskripsisp,
            dataklaim.kdsr,
            dataklaim.deskripsisr,
            dataklaim.tarifsa,
            dataklaim.tarifsd,
            dataklaim.tarifsi,
            dataklaim.tarifsp,
            dataklaim.tarifsr,
            dataklaim.tarifgrup,
            dataklaim.bytagsep,
            dataklaim.id_logik,
            dataklaim.redflag,
            dataklaim.deskripsi_redflag,
            dataklaim.keterangan_aksi,
        ]

        for col_num, cell_value in enumerate(row):
            if isinstance(cell_value, datetime.date):
                worksheet.write_datetime(row_num, col_num, cell_value, date_format)
            else:
                worksheet.write(row_num, col_num, cell_value)

    workbook.close()
    return response


def distribute_claims_to_verifikator(no_surat_bast, verifikator_list):
    """
    Fungsi untuk memindahkan data dari DataKlaimCBGMetafisik ke DataKlaimCBG
    dan membagi klaim ke verifikator berdasarkan no_surat_bast.
    """
    try:
        with transaction.atomic():
            # Dapatkan objek yang diperlukan
            no_ba_metafisik = NoBAMetafisik.objects.filter(no_surat_bast=no_surat_bast).first()
            if not no_ba_metafisik:
                return False

            register_klaim = RegisterKlaim.objects.filter(no_ba_terima=no_surat_bast).first()
            if not register_klaim:
                return False

            # Pindahkan data klaim
            move_metafisik_data_to_klaim(no_ba_metafisik, register_klaim)

            # Dapatkan queryset klaim yang baru ditambahkan
            new_claims = DataKlaimCBG.objects.filter(
                register_klaim=register_klaim,
                status=StatusDataKlaimChoices.BELUM_VER
            )

            # Distribusikan klaim ke verifikator
            distribute_to_verifikator(new_claims, verifikator_list)

            # Dapatkan queryset klaim proses
            after_claims = DataKlaimCBG.objects.filter(
                register_klaim=register_klaim,
                status=StatusDataKlaimChoices.PROSES
            )

            # Tentukan SLA
            set_claims_sla(after_claims, register_klaim)

            # is_bagi menjadi True
            no_ba_metafisik.is_bagi = True
            no_ba_metafisik.save()

        return True
    except Exception as e:
        # Log error jika diperlukan
        print(f"Error in distribute_claims_to_verifikator: {e}")
        return False


def move_metafisik_data_to_klaim(no_ba_metafisik, register_klaim):
    """
    Fungsi untuk memindahkan data dari DataKlaimCBGMetafisik ke DataKlaimCBG.
    """
    metafisik_data = DataKlaimCBGMetafisik.objects.filter(no_bast=no_ba_metafisik)
    klaim_objects = []

    for meta in metafisik_data:
        # Pastikan NOSEP unik
        no_sep = meta.nosjp
        if DataKlaimCBG.objects.filter(NOSEP=no_sep).exists():
            continue  # Lewati jika NOSEP sudah ada

        # Tentukan jenis pelayanan
        jenis_pelayanan = JenisPelayananChoices.RAWAT_INAP if meta.nmtkp == 'RITL' else JenisPelayananChoices.RAWAT_JALAN

        # Buat instance DataKlaimCBG baru
        data_klaim = DataKlaimCBG(
            register_klaim=register_klaim,
            faskes=register_klaim.faskes,
            bupel=register_klaim.bulan_pelayanan,
            ALGORITMA=meta.redflag,
            NOSEP=meta.nosjp,
            TGLSEP=meta.tgldtgsep,
            TGLPULANG=meta.tglplgsep,
            JNSPEL=jenis_pelayanan,
            NOKARTU=meta.nokapst,
            NMPESERTA=meta.nokapst,
            POLI=meta.politujsep,
            KDINACBG=meta.kdinacbgs,
            BYPENGAJUAN=meta.bytagsep or 0,
            status=StatusDataKlaimChoices.BELUM_VER,
            is_metafisik=True,
            id_metafisik=meta.id_logik,
            keterangan_aksi=meta.keterangan_aksi,
            deskripsi_metafisik=meta.deskripsi_redflag,
            indikator_metafisik=meta.indikator,
        )
        klaim_objects.append(data_klaim)

    # Bulk create klaim untuk efisiensi
    DataKlaimCBG.objects.bulk_create(klaim_objects)


def distribute_to_verifikator(claims_queryset, verifikator_list):
    """
    Fungsi untuk membagi klaim ke verifikator, memprioritaskan peserta dengan jumlah klaim terbanyak.
    """
    if not verifikator_list:
        # Jika tidak ada verifikator, klaim tidak akan ditetapkan
        return

    # Fungsi bantu untuk distribusi klaim
    def assign_claims(claims, jenis_pelayanan):
        # Ambil daftar NMPESERTA dan hitung frekuensinya
        nmpeserta_list = claims.values_list('NMPESERTA', flat=True)
        nmpeserta_counter = Counter(nmpeserta_list)
        # Urutkan NMPESERTA berdasarkan jumlah klaim terbanyak
        sorted_nmpeserta = [nmpeserta for nmpeserta, count in nmpeserta_counter.most_common()]
        index = random.randrange(len(verifikator_list))

        for nmpeserta in sorted_nmpeserta:
            claims.filter(NMPESERTA=nmpeserta, JNSPEL=jenis_pelayanan).update(
                verifikator=verifikator_list[index],
                status=StatusDataKlaimChoices.PROSES
            )
            index = (index + 1) % len(verifikator_list)

    # Distribusikan klaim Rawat Jalan
    claims_rj = claims_queryset.filter(JNSPEL=JenisPelayananChoices.RAWAT_JALAN)
    assign_claims(claims_rj, JenisPelayananChoices.RAWAT_JALAN)

    # Distribusikan klaim Rawat Inap
    claims_ri = claims_queryset.filter(JNSPEL=JenisPelayananChoices.RAWAT_INAP)
    assign_claims(claims_ri, JenisPelayananChoices.RAWAT_INAP)


def set_claims_sla(claims_queryset, register_klaim):
    """
    Fungsi untuk menetapkan tgl_SLA pada klaim berdasarkan SLA yang berlaku.
    """
    sla = SLA.objects.filter(
        jenis_klaim=register_klaim.jenis_klaim,
        kantor_cabang=register_klaim.faskes.kantor_cabang
    ).first()

    sla_date = None
    if sla:
        if register_klaim.tgl_ba_lengkap:
            sla_date = register_klaim.tgl_ba_lengkap + timedelta(days=sla.plus_hari_sla)
        elif register_klaim.tgl_terima:
            sla_date = register_klaim.tgl_terima + timedelta(days=15)
    else:
        if register_klaim.tgl_ba_lengkap:
            sla_date = register_klaim.tgl_ba_lengkap + timedelta(days=6)
        elif register_klaim.tgl_terima:
            sla_date = register_klaim.tgl_terima + timedelta(days=15)

    # Update tgl_SLA pada klaim
    if sla_date:
        claims_queryset.update(tgl_SLA=sla_date)

