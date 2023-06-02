from django.test import TestCase

from bpjs_lib.bpjs import AntrianBPJS


class DokterTestCase(TestCase):

    def test_get_data_dokter(self):
        route = 'ref/dokter'
        data = {
            'nama': 'aa'
        }
        req = AntrianBPJS(route=route)
        req.get()
        # print(req.response.text)
        print(req.data)
