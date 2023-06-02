from django.test import TestCase


from bpjs_lib.bpjs import Vclaim


class SPRITestCase(TestCase):

    def test_insert_spri(self):
        data = {
            'request':
                {
                    'noKartu': '0001116500714',
                    'kodeDokter': 31537,
                    'poliKontrol': 'BED',
                    'tglRencanaKontrol': '2021-04-13',
                    'user': 'sss'
                }
        }
        route = f'RencanaKontrol/InsertSPRI'
        req = Vclaim(route=route, json=data)
        req.post()
        print(req.response)
