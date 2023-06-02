from django.test import TestCase

from bpjs_lib.bpjs import AntrianBPJS


class AntrianTestCase(TestCase):

    def test_add_antrian(self):
        data = {
            "kodebooking": "16032021A001",
            "jenispasien": "JKN",
            "nomorkartu": "0001141325109",
            "nik": "3212345678987654",
            "nohp": "085635228888",
            "kodepoli": "ANA",
            "namapoli": "Anak",
            "pasienbaru": 0,
            "norm": "123345",
            "tanggalperiksa": "2021-01-28",
            "kodedokter": 340161,
            "namadokter": "dr Achmad Headriawan Turniadi Sp.A",
            "jampraktek": "08:00-16:00",
            "jeniskunjungan": 1,
            "nomorreferensi": "0001R0040116A000001",
            "nomorantrean": "A-12",
            "angkaantrean": 12,
            "estimasidilayani": 1615869169000,
            "sisakuotajkn": 5,
            "kuotajkn": 30,
            "sisakuotanonjkn": 5,
            "kuotanonjkn": 30,
            "keterangan": "Peserta harap 30 menit lebih awal guna pencatatan administrasi."
        }

        route = 'antrean/add'
        req = AntrianBPJS(route=route, json=data)
        req.post()
        print(req.response.text)
        print(req.data)
