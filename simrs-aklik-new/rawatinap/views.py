from bpjs_lib.bpjs import Vclaim, AntrianBPJS
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from django.utils import timezone

from icd.models import ICD10


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


def carikodedokterrawatinap(request):
    route = 'RencanaKontrol/ListSpesialistik/JnsKontrol/1/nomor/0001141325109/TglRencanaKontrol/2023-05-28'
    req = Vclaim(route=route)
    req.get()
    print(req.response.text)
    print(req.data)
    kodedokterrawatinap = req.data['list']
    return kodedokterrawatinap


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
        datakodedokterrawatinap = carikodedokterrawatinap(request)
        context = {
            'datakodedokterrawatinap': datakodedokterrawatinap,
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

        return render(request, 'rawatinap/mutasirawatinap.html', context)
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
        datakodedokterrawatinap = carikodedokterrawatinap(request)
        context = {
            'datakodedokterrawatinap': datakodedokterrawatinap,
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

        return render(request, 'rawatinap/mutasirawatinap.html', context)
    else:
        messages.info(request, 'DATA NIK TIDAK DITEMUKAN')
        return redirect('rawatinap/mutasirawatinap')


def mutasirawatinap(request):
    return render(request, 'rawatinap/mutasirawatinap.html')


@transaction.atomic
def postmutasirawatinap(request):
    route = 'RencanaKontrol/InsertSPRI'
    current_date = timezone.now()
    formatted_date = current_date.strftime('%Y-%m-%d')
    data = {
        "request":
            {
                "noKartu": "{0}".format(request.POST.get('nokartu')),
                "kodeDokter": "{0}".format(request.POST.get('kodedpjp')),
                "poliKontrol": "{0}".format(request.POST.get('kodepoli')),
                "tglRencanaKontrol": "{0}".format(formatted_date),
                "user": "DT1002R002"
            }
    }
    req = Vclaim(route=route, json=data)
    req.post()
    print(req.response.text)
    print(req.data)
    dataspri = req.data.get('noSPRI')

    route = 'Peserta/nik/3204330812880004/tglSEP/2023-05-28'
    req = Vclaim(route=route)
    req.get()
    print(req.response)
    print(req.data)
    datahakkelas = req.data.get('peserta').get('hakKelas').get('kode')
    datamr = req.data.get('peserta').get('mr').get('noMR')
    datatelp = req.data.get('peserta').get('mr').get('noTelepon')

    # formulasi rawat inap
    route = 'SEP/2.0/insert'
    data = {
        "request": {
            "t_sep": {
                "noKartu": "{0}".format(request.POST.get('nokartu')),
                "tglSep": "{0}".format(formatted_date),
                "ppkPelayanan": "1002R002",
                "jnsPelayanan": "1",  # aware of it
                "klsRawat": {
                    "klsRawatHak": "{0}".format(datahakkelas),
                    "klsRawatNaik": "",
                    "pembiayaan": "",
                    "penanggungJawab": ""
                },
                "noMR": "{0}".format(datamr),
                "rujukan": {
                    "asalRujukan": "2",
                    "tglRujukan": "{0}".format(formatted_date),
                    "noRujukan": "{0}".format(dataspri),  # perlu ada
                    "ppkRujukan": "1002R002"  # perlu ada
                },
                "catatan": "{0}".format(request.POST.get('catatan')),
                "diagAwal": "{0}".format(request.POST.get('kodeicd')),
                "poli": {
                    "tujuan": "",
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
                    "noSurat": "{0}".format(dataspri),  # perlu ada ya
                    "kodeDPJP": "{0}".format(request.POST.get('kodedpjp'))  # perlu ada
                },
                "dpjpLayan": "",  # dpjp layan dikosongkan kalo rawat inap
                "noTelp": "{0}".format(datatelp),  # nomor pasien
                "user": "DT1002R002"
            }
        }
    }
    req = Vclaim(route=route, json=data)
    req.post()
    print(req.response.text)
    print(req.data)
    print(req.data)
    print(req.data)
    print(req.data)
    print(req.data)
    messages.info(request, '{0}'.format(req.response.text))
    messages.info(request, '{0}'.format(req.response.text))
    messages.info(request, '{0}'.format(req.response.text))
    return redirect('/rawatinap/mutasirawatinap')


def daftarpasienrawatinap(request):
    route = 'RencanaKontrol/ListRencanaKontrol/tglAwal/2023-05-29/tglAkhir/2023-05-29/filter/1'
    req = Vclaim(route=route)
    req.get()
    # print(req.response.text)
    print(req.data)
    daftarpasienranap = req.data['list']
    context = {
        'daftarpasienranap': daftarpasienranap
    }
    return render(request, 'rawatinap/daftarpasienrawatinapbpjs.html', context)