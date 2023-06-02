import json

from bpjs_lib.bpjs import AntrianBPJS, Vclaim
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone

from icd.models import ICD10
from pasien.choices import (
    StatusPasienChoices,
    TipeLayanan,
    AgamaChoices,
    AsuransiChoices,
)
from daerah.models import (
    Provinsi,
    Kabupaten,
)


# Create your views here.
def daftarkunjunganrajal(request):
    current_date = timezone.now()
    formatted_date = current_date.strftime('%Y-%m-%d')
    route = 'Monitoring/Kunjungan/Tanggal/{0}/JnsPelayanan/{1}'.format(formatted_date, '2')
    req = Vclaim(route=route)
    req.get()
    print(req.data)
    daftarrajal = req.data.get('sep')
    return daftarrajal


# def daftarpasienigd(request):
#     daftarpasienrajal = daftarkunjunganrajal(request)
#     context = {
#         'daftarpasienrajal': daftarpasienrajal
#     }
#     return render(request, 'daftarpasienigd', context)


def caridatadokter(request):
    route = 'ref/dokter'
    req = AntrianBPJS(route=route)
    req.get()
    print(req.data)
    datadokter = req.data
    return datadokter


def caridataicd10(request):
    route = 'referensi/diagnosa/E10'
    req = Vclaim(route=route)
    req.get()
    req.get()
    print(req.data)
    dataicd10 = req.data
    kodeicd10 = dataicd10.get('diagnosa')
    return kodeicd10


def caridatapasienviabpjs(request):
    nokartu = request.POST.get('nokartu')
    current_date = timezone.now()
    formatted_date = current_date.strftime('%Y-%m-%d')
    route = 'Peserta/nokartu/{0}/tglSEP/{1}'.format(nokartu, formatted_date)
    req = Vclaim(route=route)
    req.get()
    print(req.response)
    if req.data:
        data = req.data
        nokartu = data['peserta']['noKartu']
        nik = data['peserta']['nik']
        nama = data['peserta']['nama']
        pisa = data['peserta']['pisa']
        sex = data['peserta']['sex']
        noMR = data['peserta']['mr']['noMR']
        noTelepon = data['peserta']['mr']['noTelepon']
        tglLahir = data['peserta']['tglLahir']
        tglCetakKartu = data['peserta']['tglCetakKartu']
        tglTAT = data['peserta']['tglTAT']
        tglTMT = data['peserta']['tglTMT']
        kodeStatusPeserta = data['peserta']['statusPeserta']['kode']
        keteranganStatusPeserta = data['peserta']['statusPeserta']['keterangan']
        kdProvider = data['peserta']['provUmum']['kdProvider']
        nmProvider = data['peserta']['provUmum']['nmProvider']
        kodeJenisPeserta = data['peserta']['jenisPeserta']['kode']
        keteranganJenisPeserta = data['peserta']['jenisPeserta']['keterangan']
        kodeHakKelas = data['peserta']['hakKelas']['kode']
        keteranganHakKelas = data['peserta']['hakKelas']['keterangan']
        umurSekarang = data['peserta']['umur']['umurSekarang']
        umurSaatPelayanan = data['peserta']['umur']['umurSaatPelayanan']
        dinsos = data['peserta']['informasi']['dinsos']
        prolanisPRB = data['peserta']['informasi']['prolanisPRB']
        noSKTM = data['peserta']['informasi']['noSKTM']
        eSEP = data['peserta']['informasi']['eSEP']
        noAsuransi = data['peserta']['cob']['noAsuransi']
        nmAsuransi = data['peserta']['cob']['nmAsuransi']
        tglTMT_COB = data['peserta']['cob']['tglTMT']
        tglTAT_COB = data['peserta']['cob']['tglTAT']
        datadokternya = caridatadokter(request)
        dataicd10nya = caridataicd10(request)
        icd10 = ICD10.objects.all()
        context = {
            'icd10': icd10,
            'dataicd10nya': dataicd10nya,
            'datadokternya': datadokternya,
            'nokartu': nokartu,
            'nik': nik,
            'nama': nama,
            'pisa': pisa,
            'sex': sex,
            'noMR': noMR,
            'noTelepon': noTelepon,
            'tglLahir': tglLahir,
            'tglCetakKartu': tglCetakKartu,
            'tglTAT': tglTAT,
            'tglTMT': tglTMT,
            'kodeStatusPeserta': kodeStatusPeserta,
            'keteranganStatusPeserta': keteranganStatusPeserta,
            'kdProvider': kdProvider,
            'nmProvider': nmProvider,
            'kodeJenisPeserta': kodeJenisPeserta,
            'keteranganJenisPeserta': keteranganJenisPeserta,
            'kodeHakKelas': kodeHakKelas,
            'keteranganHakKelas': keteranganHakKelas,
            'umurSekarang': umurSekarang,
            'umurSaatPelayanan': umurSaatPelayanan,
            'dinsos': dinsos,
            'prolanisPRB': prolanisPRB,
            'noSKTM': noSKTM,
            'eSEP': eSEP,
            'noAsuransi': noAsuransi,
            'nmAsuransi': nmAsuransi,
            'tglTMT_COB': tglTMT_COB,
            'tglTAT_COB': tglTAT_COB
        }

        return render(request, 'igd/pendaftaran-igd.html', context)
    else:
        datapasienviabpjs = None
        return datapasienviabpjs


def caridatapasienvianik(request):
    nik = request.POST.get('nik')
    current_date = timezone.now()
    formatted_date = current_date.strftime('%Y-%m-%d')
    route = 'Peserta/nik/{0}/tglSEP/{1}'.format(nik, formatted_date)
    req = Vclaim(route=route)
    req.get()
    print(req.response)
    if req.data:
        data = req.data
        nokartu = data['peserta']['noKartu']
        nik = data['peserta']['nik']
        nama = data['peserta']['nama']
        pisa = data['peserta']['pisa']
        sex = data['peserta']['sex']
        noMR = data['peserta']['mr']['noMR']
        noTelepon = data['peserta']['mr']['noTelepon']
        tglLahir = data['peserta']['tglLahir']
        tglCetakKartu = data['peserta']['tglCetakKartu']
        tglTAT = data['peserta']['tglTAT']
        tglTMT = data['peserta']['tglTMT']
        kodeStatusPeserta = data['peserta']['statusPeserta']['kode']
        keteranganStatusPeserta = data['peserta']['statusPeserta']['keterangan']
        kdProvider = data['peserta']['provUmum']['kdProvider']
        nmProvider = data['peserta']['provUmum']['nmProvider']
        kodeJenisPeserta = data['peserta']['jenisPeserta']['kode']
        keteranganJenisPeserta = data['peserta']['jenisPeserta']['keterangan']
        kodeHakKelas = data['peserta']['hakKelas']['kode']
        keteranganHakKelas = data['peserta']['hakKelas']['keterangan']
        umurSekarang = data['peserta']['umur']['umurSekarang']
        umurSaatPelayanan = data['peserta']['umur']['umurSaatPelayanan']
        dinsos = data['peserta']['informasi']['dinsos']
        prolanisPRB = data['peserta']['informasi']['prolanisPRB']
        noSKTM = data['peserta']['informasi']['noSKTM']
        eSEP = data['peserta']['informasi']['eSEP']
        noAsuransi = data['peserta']['cob']['noAsuransi']
        nmAsuransi = data['peserta']['cob']['nmAsuransi']
        tglTMT_COB = data['peserta']['cob']['tglTMT']
        tglTAT_COB = data['peserta']['cob']['tglTAT']
        datadokternya = caridatadokter(request)
        dataicd10nya = caridataicd10(request)
        icd10 = ICD10.objects.all()
        context = {
            'icd10': icd10,
            'dataicd10nya': dataicd10nya,
            'datadokternya': datadokternya,
            'nokartu': nokartu,
            'nik': nik,
            'nama': nama,
            'pisa': pisa,
            'sex': sex,
            'noMR': noMR,
            'noTelepon': noTelepon,
            'tglLahir': tglLahir,
            'tglCetakKartu': tglCetakKartu,
            'tglTAT': tglTAT,
            'tglTMT': tglTMT,
            'kodeStatusPeserta': kodeStatusPeserta,
            'keteranganStatusPeserta': keteranganStatusPeserta,
            'kdProvider': kdProvider,
            'nmProvider': nmProvider,
            'kodeJenisPeserta': kodeJenisPeserta,
            'keteranganJenisPeserta': keteranganJenisPeserta,
            'kodeHakKelas': kodeHakKelas,
            'keteranganHakKelas': keteranganHakKelas,
            'umurSekarang': umurSekarang,
            'umurSaatPelayanan': umurSaatPelayanan,
            'dinsos': dinsos,
            'prolanisPRB': prolanisPRB,
            'noSKTM': noSKTM,
            'eSEP': eSEP,
            'noAsuransi': noAsuransi,
            'nmAsuransi': nmAsuransi,
            'tglTMT_COB': tglTMT_COB,
            'tglTAT_COB': tglTAT_COB
        }

        return render(request, 'igd/pendaftaran-igd.html', context)
    else:
        messages.info(request, 'DATA NIK TIDAK DITEMUKAN')
        return redirect('/igd/pendaftaranigd')


def tambahpasienigdbpjs(request):
    current_date = timezone.now()
    formatted_date = current_date.strftime('%Y-%m-%d')
    route = 'SEP/2.0/insert'
    data = {
        "request": {
            "t_sep": {
                "noKartu": f"{request.POST.get('nokartu')}",
                "tglSep": "{0}".format(formatted_date),
                "ppkPelayanan": "1002R002",
                "jnsPelayanan": "2",
                "klsRawat": {
                    "klsRawatHak": "2",
                    "klsRawatNaik": "",
                    "pembiayaan": "",
                    "penanggungJawab": ""
                },
                "noMR": "{0}".format(request.POST.get('norm')),
                "rujukan": {
                    "asalRujukan": "2",
                    "tglRujukan": "{0}".format(formatted_date),
                    "noRujukan": "",
                    "ppkRujukan": ""
                },
                "catatan": "{0}".format(request.POST.get('catatan')),
                "diagAwal": "{0}".format(request.POST.get('kodeicd')),
                "poli": {
                    "tujuan": "IGD",
                    "eksekutif": "0"
                },
                "cob": {
                    "cob": "0"
                },
                "katarak": {
                    "katarak": "0"
                },
                "jaminan": {
                    "lakaLantas": "0",
                    "noLP": "",
                    "penjamin": {
                        "tglKejadian": "",
                        "keterangan": "",
                        "suplesi": {
                            "suplesi": "0",
                            "noSepSuplesi": "",
                            "lokasiLaka": {
                                "kdPropinsi": "",
                                "kdKabupaten": "",
                                "kdKecamatan": ""
                            }
                        }
                    }
                },
                "tujuanKunj": "0",
                "flagProcedure": "",
                "kdPenunjang": "",
                "assesmentPel": "",
                "skdp": {
                    "noSurat": "",
                    "kodeDPJP": ""
                },
                "dpjpLayan": "{0}".format(request.POST.get('kodedpjp')),
                "noTelp": "{0}".format(request.POST.get('nomorpasien')),  # nomor pasien
                "user": "DT1002R002"
            }
        }
    }
    req = Vclaim(route=route, json=data)
    req.post()
    # print(req.response.text)
    print(req.data)
    messages.info(request, 'Pasien {0} telah didaftarkan di IGD'.format(request.POST.get('namapasien')))
    return redirect('/igd/pendaftaranigd')


def pendaftaranigd(request):
    return render(request, 'igd/pendaftaran-igd.html')


def daftarpasienigd(request):
    daftarpasienigdnya = daftarkunjunganrajal(request)
    daftarpasienigdnya = reversed(daftarpasienigdnya)
    context = {
        'daftarpasienigdnya': daftarpasienigdnya
    }
    return render(request, 'igd/daftarpasienigd.html', context)
