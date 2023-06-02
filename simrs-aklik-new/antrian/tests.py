from django.test import TestCase


from bpjs_lib.bpjs import AntrianBPJS, Vclaim


# class AntrianTestCase(TestCase):
#
#     def test_antrian_pertanggal(self):
#         tanggal = '2023-05-25'
#         data = {
#    "kodebooking": "16032021A001",
#    "taskid": 1,
#    "waktu": 1616559330000,
#    "jenisresep": "Tidak ada/Racikan/Non racikan"
# }
#         route = f'antrean/updatewaktu'
#         req = AntrianBPJS(route=route, json=data)
#         req.post()
#         print(req.response.text)
#         print(req.data)



class SEPTestCase(TestCase):

    # def test_cari_data_peserta_dngn_nik(self):
    #     p1 = 111111111111111
    #     p2 = '2022-02-02'
    #     route = f'Peserta/nik/{p1}/tglSEP/{p2}'
    #     req = Vclaim(route=route)
    #     req.get()
    #     print(req.response.json())
    #     print(req.data)

    # def test_insert_rujukan_khusus(self):
    #     data = {
    #      "noRujukan": "0301U0331019P003283",
    #      "diagnosa": [
    #              {"kode": "P;N18"},
    #              {"kode": "S;N18.1"}
    #      ],
    #     "procedure":  [
    #              {"kode": "39.95"}
    #      ],
    #      "user": "Coba Ws"
    # }
    #     route = f'Rujukan/Khusus/insert'
    #     req = Vclaim(route=route, json=data)
    #     req.post()
    #     print(req.response.text)


    def test_update_prb(self):
        route = f'PRB/Update'
        data = {

              "t_prb":{
                 "noSrb":"9118924",
                 "noSep":"0301R0011117V000008",
                 "alamat":"jl. Merdekah",
                 "email":"emailkudisadap@gmail.com",
                 "kodeDPJP":"271190",
                 "keterangan":"Capek Kerja",
                 "saran":"Pasien harus Cuti,Kecapekan Kerja dan Kerja.",
                 "user":"123456",
                 "obat":[
                    {
                       "kdObat": "00196999124",
                       "signa1": "3",
                       "signa2": "1",
                       "jmlObat": "5"
                    },
                    {
                       "kdObat":"00011999918",
                       "signa1":"3",
                       "signa2":"1",
                       "jmlObat":"10"
                    }
                 ]
              }
           }

        req = Vclaim(route=route, data=data)
        req.put()
        print(req.response)
