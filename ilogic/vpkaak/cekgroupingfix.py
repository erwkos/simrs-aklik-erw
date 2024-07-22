import json
import time

import browsercookie
import requests
import hashlib
import random
import re
import datetime
import urllib.parse
import ast
from urllib.parse import urlparse, parse_qs

import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction


def get_hash(password):
    salt = hashlib.md5(str(random.random()).encode('utf-8')).hexdigest()
    hashed_password = hashlib.md5(
        (salt + hashlib.md5(password.encode('utf-8')).hexdigest()).encode('utf-8')).hexdigest()
    return hashed_password, salt


def grouping(gender=str, umur=str, no_sep=str, no_peserta=str, tipe_rawat=str,
             kelas_rawat=str, diagnosa=str, prosedur=str, sp=str,
             sr=str, si=str, sd=str,
             is_bayi=bool, birth_weight=str, tanggallahirbayi=str, Tgldtgsjp=str, Tglplgsjp=str, rs_tarif=str):

    with ((transaction.atomic())):
        session = requests.Session()

        login_url = 'http://grey.lerix.co.id/E-Klaim/login.php'

        username = 'inacbg'
        password = 'inacbg'

        hashed_password, salt = get_hash(password)

        payload = {
            'login': username,
            'rndx': hashed_password,
            'hash': 1,
            'rnd': salt
        }

        response = session.get(login_url, params=payload)
        # print(response.text)

        # pattern_rs_tarif = r'<div id=[\'"]banner_hospital_class_reg[\'"] style=[\'"]font-size:0\.6em;[\'"]>KELAS "(.*?)" &bull;'

        # data_list_match_rs_tarif = re.findall(pattern_rs_tarif, response.text)

        # rs_tarif_founded = rs_tarif

        # if data_list_match_rs_tarif == "A PEMERINTAH":
        #     rs_tarif_founded = "AP"
        # if data_list_match_rs_tarif == "B PEMERINTAH":
        #     rs_tarif_founded = "BP"
        # if data_list_match_rs_tarif == "C PEMERINTAH":
        #     rs_tarif_founded = "CP"
        # if data_list_match_rs_tarif == "D PEMERINTAH":
        #     rs_tarif_founded = "DP"
        # if data_list_match_rs_tarif == "E PEMERINTAH":
        #     rs_tarif_founded = "EP"
        #
        # if data_list_match_rs_tarif == "A SWASTA":
        #     rs_tarif_founded = "AS"
        # if data_list_match_rs_tarif == "B SWASTA":
        #     rs_tarif_founded = "BS"
        # if data_list_match_rs_tarif == "C SWASTA":
        #     rs_tarif_founded = "CS"
        # if data_list_match_rs_tarif == "D SWASTA":
        #     rs_tarif_founded = "DS"
        # if data_list_match_rs_tarif == "E SWASTA":
        #     rs_tarif_founded = "ES"

        # parsed_url = urlparse(response.url)
        # query_params = parse_qs(parsed_url.query)
        # rand_login = query_params.get('rand', [None])[0]
        # print('Rand Login:', rand_login)
        Tgldtgsjp = datetime.datetime.strptime(Tgldtgsjp, '%Y-%m-%d').date()
        Tglplgsjp = datetime.datetime.strptime(Tglplgsjp, '%Y-%m-%d').date()

        if response.url.startswith('http://grey.lerix.co.id/E-Klaim/index.php') and 'success=1' in response.url:
            try:
                # print('Login successful!')
                # print(f'Redirected to: {response.url}')

                sekarang = datetime.datetime.now()
                waktusekarang = int(sekarang.timestamp() * 1000)
                mrn = no_peserta
                person_nm = 'BPJS Kesehatan'
                person_nm = urllib.parse.quote(person_nm)
                gender = str(gender)  # m berarti laki-laki ---- f berarti perempuan
                if is_bayi is True:
                    birth_dttm = f"{tanggallahirbayi}"
                elif umur == "0" or umur == 0:
                    date = Tgldtgsjp - datetime.timedelta(days=7)
                    # Memisahkan tahun, bulan, dan hari
                    tahun = str(date.year)
                    bulan = str(date.month)
                    hari = str(date.day)
                    birth_dttm = f'{tahun}-{bulan}-{hari}'

                    if tanggallahirbayi:
                        birth_dttm = tanggallahirbayi
                        # print(birth_dttm, Tgldtgsjp, birth_weight)
                    # birth_dttm = '2023-01-01'
                else:
                    tahun = 2024 - int(umur)
                    # print(umur)
                    bulan = '11'
                    hari = '11'
                    # jam = '11'
                    # menit = '11'
                    # detik = '11'
                    birth_dttm = f'{tahun}-{bulan}-{hari}'
                new_patient_url = 'http://grey.lerix.co.id/E-Klaim/index.php?X_his=padm&slpat_new_pat=1'
                session.get(new_patient_url)

                add_new_patient_url = f'http://grey.lerix.co.id/E-Klaim/ajaxreq.php?ac=pt&ff=app_savePerson&ffargs[0]=mrn%255E%255E{mrn}%2540%2540person_nm%255E%255E{person_nm}%2540%2540adm_gender_cd%255E%255E{gender}%2540%2540birth_dttm%255E%255E{birth_dttm}%25200%253A0%253A0&ffargs[1]=new&ffargs[2]=&ffrnd={waktusekarang}'
                # add_new_patient_url = f'http://grey.lerix.co.id/E-Klaim/ajaxreq.php?/E-Klaim/ajaxreq.php?ac=pt&ff=app_savePerson&ffargs[0]=mrn%255E%255E18325749%2540%2540person_nm%255E%255EBPJS%2520Kesehatan%2540%2540adm_gender_cd%255E%255Em%2540%2540birth_dttm%255E%255E1988-6-17%25200%253A0%253A0&ffargs[1]=new&ffargs[2]=&ffrnd=1718636053065'
                session.get(add_new_patient_url)

                no_peserta = str(no_peserta)
                no_sep = str(no_sep)

                icd10 = str(diagnosa)  # melahirkan O80.0|Z37.0
                icd9 = str(prosedur)  # 96.71 / 96.72

                # icd10 = urllib.parse.unquote(icd10)
                # print(icd10)
                # icd9 = urllib.parse.unquote(icd9)
                # print(icd9)

                # rs_tarif = rs_tarif_founded
                # print('Tarif RS dari cek gropuing', rs_tarif)

                icd10 = urllib.parse.quote(icd10)

                icd9 = urllib.parse.quote(icd9)

                birth_weight = birth_weight

                birth_weight = urllib.parse.quote(birth_weight)

                add_1_klaim_baru = 'http://grey.lerix.co.id/E-Klaim/ajaxreq.php?ac=pt&ff=app_newAdmission'
                add_1_klaim_baru_response = session.post(add_1_klaim_baru)
                data = add_1_klaim_baru_response.text
                # print("Save Data Admission:", data)
                match = re.search(r'\[(\d+),', data)
                if match:
                    number = match.group(1)
                    # print(f"Angka yang ditemukan: {number}")
                # else:
                #     # print("Angka tidak ditemukan.")
                add_2_klaim_baru = f'http://grey.lerix.co.id/E-Klaim/ajaxreq.php?ac=pt&ff=app_editAdmission&ffargs[0]={number}'
                session.post(add_2_klaim_baru)
                data_list_match_option = 'DR X'
                dpjp_option = urllib.parse.quote(str(data_list_match_option))
                dpjp_option = urllib.parse.quote(str(dpjp_option))

                # sending1 = f'http://grey.lerix.co.id/E-Klaim/ajaxreq.php?ac=pt&ff=app_getUploadedFile&ffargs[0]={number}&ffargs[1]=resume_medis'
                # sending2 = f'http://grey.lerix.co.id/E-Klaim/ajaxreq.php?ac=pt&ff=app_getUploadedFile&ffargs[0]={number}&ffargs[1]=ruang_rawat'
                # sending3 = f'http://grey.lerix.co.id/E-Klaim/ajaxreq.php?ac=pt&ff=app_getUploadedFile&ffargs[0]={number}&ffargs[1]=radiologi'
                # sending4 = f'http://grey.lerix.co.id/E-Klaim/ajaxreq.php?ac=pt&ff=app_getUploadedFile&ffargs[0]={number}&ffargs[1]=resep_obat'
                # sending5 = f'http://grey.lerix.co.id/E-Klaim/ajaxreq.php?ac=pt&ff=app_getUploadedFile&ffargs[0]={number}&ffargs[1]=laboratorium'
                # sending6 = f'http://grey.lerix.co.id/E-Klaim/ajaxreq.php?ac=pt&ff=app_getUploadedFile&ffargs[0]={number}&ffargs[1]=penunjang_lain'
                # sending7 = f'http://grey.lerix.co.id/E-Klaim/ajaxreq.php?ac=pt&ff=app_getUploadedFile&ffargs[0]={number}&ffargs[1]=tagihan'
                # sending8 = f'http://grey.lerix.co.id/E-Klaim/ajaxreq.php?ac=pt&ff=app_getUploadedFile&ffargs[0]={number}&ffargs[1]=kartu_identitas'
                # sending9 = f'http://grey.lerix.co.id/E-Klaim/ajaxreq.php?ac=pt&ff=app_getUploadedFile&ffargs[0]={number}&ffargs[1]=dokumen_kipi'
                # sending10 = f'http://grey.lerix.co.id/E-Klaim/ajaxreq.php?ac=pt&ff=app_getUploadedFile&ffargs[0]={number}&ffargs[1]=bebas_biaya'
                # sending11 = f'http://grey.lerix.co.id/E-Klaim/ajaxreq.php?ac=pt&ff=app_getUploadedFile&ffargs[0]={number}&ffargs[1]=surat_kematian'
                # sending12 = f'http://grey.lerix.co.id/E-Klaim/ajaxreq.php?ac=pt&ff=app_getUploadedFile&ffargs[0]={number}&ffargs[1]=lain_lain'
                # sending13 = f'http://grey.lerix.co.id/E-Klaim/ajaxreq.php?ac=pt&ff=app_setGrouperTab&ffargs[0]=0'
                # session.post(sending1)
                # session.post(sending2)
                # session.post(sending3)
                # session.post(sending4)
                # session.post(sending5)
                # session.post(sending6)
                # session.post(sending7)
                # session.post(sending8)
                # session.post(sending9)
                # session.post(sending10)
                # session.post(sending11)
                # session.post(sending12)
                # session.post(sending13)
                # send1_grouping_url = f'http://grey.lerix.co.id/E-Klaim/ajaxreq.php?ac=pt&ff=app_saveAdmission&ffargs[0]={number}&ffargs[1]=no_kartu%255E%255E{no_peserta}%2540%2540no_sep%255E%255E{no_sep}%2540%2540admission_type%255E%255E{tipe_rawat}%2540%2540tariff_class%255E%255E{kelas_rawat}%2540%2540admission_dttm%255E%255E{sekarang.year}-{sekarang.month:02}-{sekarang.day:02}%2520{sekarang.hour:02}%253A{sekarang.minute:02}%253A{sekarang.second:02}%2540%2540discharge_dttm%255E%255E{sekarang.year}-{sekarang.month:02}-{sekarang.day:02}%2520{sekarang.hour:02}%253A{sekarang.minute:02}%253A{sekarang.second}%2540%2540episodes%255E%255E%2540%2540cc_ind%255E%255E0%2540%2540akses_naat%255E%255EC%2540%2540isoman_ind%255E%255E0%2540%2540rs_darurat_ind%255E%255E0%2540%2540co_insidence_ind%255E%255E0%2540%2540cgrp_rs_darurat_ind%255E%255E0%2540%2540cgrp_isoman_ind%255E%255E0%2540%2540upgrade_class_los%255E%255E0%2540%2540ventilator_start_dttm%255E%255E0000-00-00%252000%253A00%253A00%2540%2540ventilator_stop_dttm%255E%255E0000-00-00%252000%253A00%253A00%2540%2540icu_los%255E%255E0%2540%2540birth_weight%255E%255E{birth_weight}%2540%2540adl1%255E%255E12%2540%2540adl2%255E%255E12%2540%2540jkn_sitb_noreg%255E%255E%2540%2540covid19_no_sep%255E%255E%2540%2540billing_amount_pex%255E%255E0%2540%2540billing_amount%255E%255E1000000%2540%2540procedure_amt%255E%255E1%252C000%252C000%2540%2540surgical_amt%255E%255E0%2540%2540consul_amt%255E%255E0%2540%2540expert_amt%255E%255E0%2540%2540nursing_amt%255E%255E0%2540%2540ancillary_amt%255E%255E0%2540%2540radiology_amt%255E%255E0%2540%2540laboratory_amt%255E%255E0%2540%2540blood_amt%255E%255E0%2540%2540rehab_amt%255E%255E0%2540%2540room_amt%255E%255E0%2540%2540intensive_amt%255E%255E0%2540%2540drug_amt%255E%255E0%2540%2540drug_chronic_amt%255E%255E0%2540%2540drug_chemo_amt%255E%255E0%2540%2540device_amt%255E%255E0%2540%2540consumable_amt%255E%255E0%2540%2540device_rent_amt%255E%255E0%2540%2540terapi_konvalesen%255E%255E0%2540%2540panelitem_1011_3%255E%255E{icd10}%2540%2540panelitem_1012_1%255E%255E{icd9}%2540%2540panelitem_1011_4%255E%255E%2540%2540panelitem_1012_2%255E%255E%2540%2540jkn_sistole%255E%255E0%2540%2540jkn_diastole%255E%255E0%2540%2540jkn_apgar_1_appearance%255E%255E%2540%2540jkn_apgar_1_pulse%255E%255E%2540%2540jkn_apgar_1_grimace%255E%255E%2540%2540jkn_apgar_1_activity%255E%255E%2540%2540jkn_apgar_1_respiration%255E%255E%2540%2540jkn_apgar_5_appearance%255E%255E%2540%2540jkn_apgar_5_pulse%255E%255E%2540%2540jkn_apgar_5_grimace%255E%255E%2540%2540jkn_apgar_5_activity%255E%255E%2540%2540jkn_apgar_5_respiration%255E%255E%2540%2540jkn_usia_kehamilan%255E%255E%2540%2540jkn_gravida%255E%255E%2540%2540jkn_partus%255E%255E%2540%2540jkn_abortus%255E%255E%2540%2540jkn_onset_kontraksi%255E%255Espontan%2540%2540nomor_rujukan%255E%255E%2540%2540kode_perujuk%255E%255E%2540%2540cara_masuk%255E%255Erujukan_fktp%2540%2540usia_kehamilan%255E%255E0%2540%2540sistole%255E%255E0%2540%2540diastole%255E%255E0%2540%2540gravida%255E%255E0%2540%2540partus%255E%255E0%2540%2540abortus%255E%255E0%2540%2540onset_kontraksi%255E%255Espontan%2540%2540riwayat_sc%255E%255E0%2540%2540kuretase%255E%255E0%2540%2540nama_operasi%255E%255E%2540%2540payplan_id%255E%255E3%2540%2540cob_id%255E%255E-%2540%2540cara_masuk%255E%255Egp%2540%2540bayi_lahir_status_cd%255E%255E1%2540%2540covid19_status_cd%255E%255E4%2540%2540discharge%255E%255Ehome%2540%2540attending_doctor%255E%255E1%257CDR%2520A%2540%2540rs_tariff%255E%255E{rs_tarif}%2540%2540sp%255E%255E{sp}%2540%2540sr%255E%255E{sr}%2540%2540si%255E%255E{si}%2540%2540sd%255E%255E{sd}%2540%2540anamnesa%255E%255E%2540%2540indikasi_ranap%255E%255E%2540%2540diagnosa_primer%255E%255E%2540%2540diagnosa_sekunder%255E%255E%2540%2540prosedur%255E%255E%2540%2540laporan_operasi%255E%255E'
                # send2_grouping_url = f'http://grey.lerix.co.id/E-Klaim/ajaxreq.php?ac=pt&ff=app_grouper&ffargs[0]={number}&ffargs[1]=no_kartu%255E%255E{no_peserta}%2540%2540no_sep%255E%255E{no_sep}%2540%2540admission_type%255E%255E{tipe_rawat}%2540%2540tariff_class%255E%255E{kelas_rawat}%2540%2540admission_dttm%255E%255E{sekarang.year}-{sekarang.month:02}-{sekarang.day:02}%2520{sekarang.hour:02}%253A{sekarang.minute:02}%253A{sekarang.second:02}%2540%2540discharge_dttm%255E%255E{sekarang.year}-{sekarang.month:02}-{sekarang.day:02}%2520{sekarang.hour:02}%253A{sekarang.minute:02}%253A{sekarang.second:02}%2540%2540episodes%255E%255E%2540%2540cc_ind%255E%255E0%2540%2540akses_naat%255E%255EC%2540%2540isoman_ind%255E%255E0%2540%2540rs_darurat_ind%255E%255E0%2540%2540co_insidence_ind%255E%255E0%2540%2540cgrp_rs_darurat_ind%255E%255E0%2540%2540cgrp_isoman_ind%255E%255E0%2540%2540upgrade_class_los%255E%255E0%2540%2540ventilator_start_dttm%255E%255E0000-00-00%252000%253A00%253A00%2540%2540ventilator_stop_dttm%255E%255E0000-00-00%252000%253A00%253A00%2540%2540icu_los%255E%255E0%2540%2540birth_weight%255E%255E{birth_weight}%2540%2540adl1%255E%255E12%2540%2540adl2%255E%255E12%2540%2540jkn_sitb_noreg%255E%255E%2540%2540covid19_no_sep%255E%255E%2540%2540billing_amount_pex%255E%255E0%2540%2540billing_amount%255E%255E1000000%2540%2540procedure_amt%255E%255E1%252C000%252C000%2540%2540surgical_amt%255E%255E0%2540%2540consul_amt%255E%255E0%2540%2540expert_amt%255E%255E0%2540%2540nursing_amt%255E%255E0%2540%2540ancillary_amt%255E%255E0%2540%2540radiology_amt%255E%255E0%2540%2540laboratory_amt%255E%255E0%2540%2540blood_amt%255E%255E0%2540%2540rehab_amt%255E%255E0%2540%2540room_amt%255E%255E0%2540%2540intensive_amt%255E%255E0%2540%2540drug_amt%255E%255E0%2540%2540drug_chronic_amt%255E%255E0%2540%2540drug_chemo_amt%255E%255E0%2540%2540device_amt%255E%255E0%2540%2540consumable_amt%255E%255E0%2540%2540device_rent_amt%255E%255E0%2540%2540terapi_konvalesen%255E%255E0%2540%2540panelitem_1011_3%255E%255E{icd10}%2540%2540panelitem_1012_1%255E%255E{icd9}%2540%2540panelitem_1011_4%255E%255E%2540%2540panelitem_1012_2%255E%255E%2540%2540jkn_sistole%255E%255E0%2540%2540jkn_diastole%255E%255E0%2540%2540jkn_apgar_1_appearance%255E%255E%2540%2540jkn_apgar_1_pulse%255E%255E%2540%2540jkn_apgar_1_grimace%255E%255E%2540%2540jkn_apgar_1_activity%255E%255E%2540%2540jkn_apgar_1_respiration%255E%255E%2540%2540jkn_apgar_5_appearance%255E%255E%2540%2540jkn_apgar_5_pulse%255E%255E%2540%2540jkn_apgar_5_grimace%255E%255E%2540%2540jkn_apgar_5_activity%255E%255E%2540%2540jkn_apgar_5_respiration%255E%255E%2540%2540jkn_usia_kehamilan%255E%255E0%2540%2540jkn_gravida%255E%255E0%2540%2540jkn_partus%255E%255E0%2540%2540jkn_abortus%255E%255E0%2540%2540jkn_onset_kontraksi%255E%255Espontan%2540%2540nomor_rujukan%255E%255E%2540%2540kode_perujuk%255E%255E%2540%2540cara_masuk%255E%255Erujukan_fktp%2540%2540usia_kehamilan%255E%255E0%2540%2540sistole%255E%255E0%2540%2540diastole%255E%255E0%2540%2540gravida%255E%255E0%2540%2540partus%255E%255E0%2540%2540abortus%255E%255E0%2540%2540onset_kontraksi%255E%255Espontan%2540%2540riwayat_sc%255E%255E0%2540%2540kuretase%255E%255E0%2540%2540nama_operasi%255E%255E%2540%2540payplan_id%255E%255E3%2540%2540cob_id%255E%255E-%2540%2540cara_masuk%255E%255Egp%2540%2540bayi_lahir_status_cd%255E%255E1%2540%2540covid19_status_cd%255E%255E4%2540%2540discharge%255E%255Ehome%2540%2540attending_doctor%255E%255E1%257CDR%2520A%2540%2540rs_tariff%255E%255E{rs_tarif}%2540%2540sp%255E%255E{sp}%2540%2540sr%255E%255E{sr}%2540%2540si%255E%255E{si}%2540%2540sd%255E%255E{sd}%2540%2540anamnesa%255E%255E%2540%2540indikasi_ranap%255E%255E%2540%2540diagnosa_primer%255E%255E%2540%2540diagnosa_sekunder%255E%255E%2540%2540prosedur%255E%255E%2540%2540laporan_operasi%255E%255E'
                # tgl saatini
                # send1_grouping_url = f'http://grey.lerix.co.id/E-Klaim/ajaxreq.php?ac=pt&ff=app_saveAdmission&ffargs[0]={number}&ffargs[1]=no_kartu%255E%255E{no_peserta}%2540%2540no_sep%255E%255E{no_sep}%2540%2540admission_type%255E%255E{tipe_rawat}%2540%2540tariff_class%255E%255E{kelas_rawat}%2540%2540admission_dttm%255E%255E{sekarang.year}-{sekarang.month:02}-{sekarang.day:02}%2520{sekarang.hour:02}%253A{sekarang.minute:02}%253A{sekarang.second:02}%2540%2540discharge_dttm%255E%255E{sekarang.year}-{sekarang.month:02}-{sekarang.day:02}%2520{sekarang.hour:02}%253A{sekarang.minute:02}%253A{sekarang.second}%2540%2540episodes%255E%255E%2540%2540cc_ind%255E%255E0%2540%2540akses_naat%255E%255EC%2540%2540isoman_ind%255E%255E0%2540%2540rs_darurat_ind%255E%255E0%2540%2540co_insidence_ind%255E%255E0%2540%2540cgrp_rs_darurat_ind%255E%255E0%2540%2540cgrp_isoman_ind%255E%255E0%2540%2540upgrade_class_los%255E%255E0%2540%2540ventilator_start_dttm%255E%255E0000-00-00%252000%253A00%253A00%2540%2540ventilator_stop_dttm%255E%255E0000-00-00%252000%253A00%253A00%2540%2540icu_los%255E%255E0%2540%2540birth_weight%255E%255E{birth_weight}%2540%2540adl1%255E%255E12%2540%2540adl2%255E%255E12%2540%2540jkn_sitb_noreg%255E%255E%2540%2540covid19_no_sep%255E%255E%2540%2540billing_amount_pex%255E%255E0%2540%2540billing_amount%255E%255E1000000%2540%2540procedure_amt%255E%255E1%252C000%252C000%2540%2540surgical_amt%255E%255E0%2540%2540consul_amt%255E%255E0%2540%2540expert_amt%255E%255E0%2540%2540nursing_amt%255E%255E0%2540%2540ancillary_amt%255E%255E0%2540%2540radiology_amt%255E%255E0%2540%2540laboratory_amt%255E%255E0%2540%2540blood_amt%255E%255E0%2540%2540rehab_amt%255E%255E0%2540%2540room_amt%255E%255E0%2540%2540intensive_amt%255E%255E0%2540%2540drug_amt%255E%255E0%2540%2540drug_chronic_amt%255E%255E0%2540%2540drug_chemo_amt%255E%255E0%2540%2540device_amt%255E%255E0%2540%2540consumable_amt%255E%255E0%2540%2540device_rent_amt%255E%255E0%2540%2540terapi_konvalesen%255E%255E0%2540%2540panelitem_1011_3%255E%255E{icd10}%2540%2540panelitem_1012_1%255E%255E{icd9}%2540%2540panelitem_1011_4%255E%255E%2540%2540panelitem_1012_2%255E%255E%2540%2540jkn_sistole%255E%255E0%2540%2540jkn_diastole%255E%255E0%2540%2540jkn_apgar_1_appearance%255E%255E%2540%2540jkn_apgar_1_pulse%255E%255E%2540%2540jkn_apgar_1_grimace%255E%255E%2540%2540jkn_apgar_1_activity%255E%255E%2540%2540jkn_apgar_1_respiration%255E%255E%2540%2540jkn_apgar_5_appearance%255E%255E%2540%2540jkn_apgar_5_pulse%255E%255E%2540%2540jkn_apgar_5_grimace%255E%255E%2540%2540jkn_apgar_5_activity%255E%255E%2540%2540jkn_apgar_5_respiration%255E%255E%2540%2540jkn_usia_kehamilan%255E%255E%2540%2540jkn_gravida%255E%255E%2540%2540jkn_partus%255E%255E%2540%2540jkn_abortus%255E%255E%2540%2540jkn_onset_kontraksi%255E%255Espontan%2540%2540nomor_rujukan%255E%255E%2540%2540kode_perujuk%255E%255E%2540%2540cara_masuk%255E%255Erujukan_fktp%2540%2540usia_kehamilan%255E%255E0%2540%2540sistole%255E%255E0%2540%2540diastole%255E%255E0%2540%2540gravida%255E%255E0%2540%2540partus%255E%255E0%2540%2540abortus%255E%255E0%2540%2540onset_kontraksi%255E%255Espontan%2540%2540riwayat_sc%255E%255E0%2540%2540kuretase%255E%255E0%2540%2540nama_operasi%255E%255E%2540%2540payplan_id%255E%255E3%2540%2540cob_id%255E%255E-%2540%2540cara_masuk%255E%255Egp%2540%2540bayi_lahir_status_cd%255E%255E1%2540%2540covid19_status_cd%255E%255E4%2540%2540discharge%255E%255Ehome%2540%2540attending_doctor%255E%255E1%257C{dpjp_option}%2540%2540rs_tariff%255E%255E{rs_tarif}%2540%2540sp%255E%255ENone%2540%2540sr%255E%255ENone%2540%2540si%255E%255ENone%2540%2540sd%255E%255ENone%2540%2540anamnesa%255E%255E%2540%2540indikasi_ranap%255E%255E%2540%2540diagnosa_primer%255E%255E%2540%2540diagnosa_sekunder%255E%255E%2540%2540prosedur%255E%255E%2540%2540laporan_operasi%255E%255E'
                # send2_grouping_url = f'http://grey.lerix.co.id/E-Klaim/ajaxreq.php?ac=pt&ff=app_grouper&ffargs[0]={number}&ffargs[1]=no_kartu%255E%255E{no_peserta}%2540%2540no_sep%255E%255E{no_sep}%2540%2540admission_type%255E%255E{tipe_rawat}%2540%2540tariff_class%255E%255E{kelas_rawat}%2540%2540admission_dttm%255E%255E{sekarang.year}-{sekarang.month:02}-{sekarang.day:02}%2520{sekarang.hour:02}%253A{sekarang.minute:02}%253A{sekarang.second:02}%2540%2540discharge_dttm%255E%255E{sekarang.year}-{sekarang.month:02}-{sekarang.day:02}%2520{sekarang.hour:02}%253A{sekarang.minute:02}%253A{sekarang.second:02}%2540%2540episodes%255E%255E%2540%2540cc_ind%255E%255E0%2540%2540akses_naat%255E%255EC%2540%2540isoman_ind%255E%255E0%2540%2540rs_darurat_ind%255E%255E0%2540%2540co_insidence_ind%255E%255E0%2540%2540cgrp_rs_darurat_ind%255E%255E0%2540%2540cgrp_isoman_ind%255E%255E0%2540%2540upgrade_class_los%255E%255E0%2540%2540ventilator_start_dttm%255E%255E0000-00-00%252000%253A00%253A00%2540%2540ventilator_stop_dttm%255E%255E0000-00-00%252000%253A00%253A00%2540%2540icu_los%255E%255E0%2540%2540birth_weight%255E%255E{birth_weight}%2540%2540adl1%255E%255E12%2540%2540adl2%255E%255E12%2540%2540jkn_sitb_noreg%255E%255E%2540%2540covid19_no_sep%255E%255E%2540%2540billing_amount_pex%255E%255E0%2540%2540billing_amount%255E%255E1000000%2540%2540procedure_amt%255E%255E1%252C000%252C000%2540%2540surgical_amt%255E%255E0%2540%2540consul_amt%255E%255E0%2540%2540expert_amt%255E%255E0%2540%2540nursing_amt%255E%255E0%2540%2540ancillary_amt%255E%255E0%2540%2540radiology_amt%255E%255E0%2540%2540laboratory_amt%255E%255E0%2540%2540blood_amt%255E%255E0%2540%2540rehab_amt%255E%255E0%2540%2540room_amt%255E%255E0%2540%2540intensive_amt%255E%255E0%2540%2540drug_amt%255E%255E0%2540%2540drug_chronic_amt%255E%255E0%2540%2540drug_chemo_amt%255E%255E0%2540%2540device_amt%255E%255E0%2540%2540consumable_amt%255E%255E0%2540%2540device_rent_amt%255E%255E0%2540%2540terapi_konvalesen%255E%255E0%2540%2540panelitem_1011_3%255E%255E{icd10}%2540%2540panelitem_1012_1%255E%255E{icd9}%2540%2540panelitem_1011_4%255E%255E%2540%2540panelitem_1012_2%255E%255E%2540%2540jkn_sistole%255E%255E0%2540%2540jkn_diastole%255E%255E0%2540%2540jkn_apgar_1_appearance%255E%255E%2540%2540jkn_apgar_1_pulse%255E%255E%2540%2540jkn_apgar_1_grimace%255E%255E%2540%2540jkn_apgar_1_activity%255E%255E%2540%2540jkn_apgar_1_respiration%255E%255E%2540%2540jkn_apgar_5_appearance%255E%255E%2540%2540jkn_apgar_5_pulse%255E%255E%2540%2540jkn_apgar_5_grimace%255E%255E%2540%2540jkn_apgar_5_activity%255E%255E%2540%2540jkn_apgar_5_respiration%255E%255E%2540%2540jkn_usia_kehamilan%255E%255E0%2540%2540jkn_gravida%255E%255E0%2540%2540jkn_partus%255E%255E0%2540%2540jkn_abortus%255E%255E0%2540%2540jkn_onset_kontraksi%255E%255Espontan%2540%2540nomor_rujukan%255E%255E%2540%2540kode_perujuk%255E%255E%2540%2540cara_masuk%255E%255Erujukan_fktp%2540%2540usia_kehamilan%255E%255E0%2540%2540sistole%255E%255E0%2540%2540diastole%255E%255E0%2540%2540gravida%255E%255E0%2540%2540partus%255E%255E0%2540%2540abortus%255E%255E0%2540%2540onset_kontraksi%255E%255Espontan%2540%2540riwayat_sc%255E%255E0%2540%2540kuretase%255E%255E0%2540%2540nama_operasi%255E%255E%2540%2540payplan_id%255E%255E3%2540%2540cob_id%255E%255E-%2540%2540cara_masuk%255E%255Egp%2540%2540bayi_lahir_status_cd%255E%255E1%2540%2540covid19_status_cd%255E%255E4%2540%2540discharge%255E%255Ehome%2540%2540attending_doctor%255E%255E1%257C{dpjp_option}%2540%2540rs_tariff%255E%255E{rs_tarif}%2540%2540sp%255E%255ENone%2540%2540sr%255E%255ENone%2540%2540si%255E%255ENone%2540%2540sd%255E%255ENone%2540%2540anamnesa%255E%255E%2540%2540indikasi_ranap%255E%255E%2540%2540diagnosa_primer%255E%255E%2540%2540diagnosa_sekunder%255E%255E%2540%2540prosedur%255E%255E%2540%2540laporan_operasi%255E%255E'
                # tgl sep dtg dan plg
                send1_grouping_url = f'http://grey.lerix.co.id/E-Klaim/ajaxreq.php?ac=pt&ff=app_saveAdmission&ffargs[0]={number}&ffargs[1]=no_kartu%255E%255E{no_peserta}%2540%2540no_sep%255E%255E{no_sep}%2540%2540admission_type%255E%255E{tipe_rawat}%2540%2540tariff_class%255E%255E{kelas_rawat}%2540%2540admission_dttm%255E%255E{Tgldtgsjp.year}-{Tgldtgsjp.month:02}-{Tgldtgsjp.day:02}%2520{sekarang.hour:02}%253A{sekarang.minute:02}%253A{sekarang.second:02}%2540%2540discharge_dttm%255E%255E{Tglplgsjp.year}-{Tglplgsjp.month:02}-{Tglplgsjp.day:02}%2520{sekarang.hour:02}%253A{sekarang.minute:02}%253A{sekarang.second}%2540%2540episodes%255E%255E%2540%2540cc_ind%255E%255E0%2540%2540akses_naat%255E%255EC%2540%2540isoman_ind%255E%255E0%2540%2540rs_darurat_ind%255E%255E0%2540%2540co_insidence_ind%255E%255E0%2540%2540cgrp_rs_darurat_ind%255E%255E0%2540%2540cgrp_isoman_ind%255E%255E0%2540%2540upgrade_class_los%255E%255E0%2540%2540ventilator_start_dttm%255E%255E0000-00-00%252000%253A00%253A00%2540%2540ventilator_stop_dttm%255E%255E0000-00-00%252000%253A00%253A00%2540%2540icu_los%255E%255E0%2540%2540birth_weight%255E%255E{birth_weight}%2540%2540adl1%255E%255E12%2540%2540adl2%255E%255E12%2540%2540jkn_sitb_noreg%255E%255E%2540%2540covid19_no_sep%255E%255E%2540%2540billing_amount_pex%255E%255E0%2540%2540billing_amount%255E%255E1000000%2540%2540procedure_amt%255E%255E1%252C000%252C000%2540%2540surgical_amt%255E%255E0%2540%2540consul_amt%255E%255E0%2540%2540expert_amt%255E%255E0%2540%2540nursing_amt%255E%255E0%2540%2540ancillary_amt%255E%255E0%2540%2540radiology_amt%255E%255E0%2540%2540laboratory_amt%255E%255E0%2540%2540blood_amt%255E%255E0%2540%2540rehab_amt%255E%255E0%2540%2540room_amt%255E%255E0%2540%2540intensive_amt%255E%255E0%2540%2540drug_amt%255E%255E0%2540%2540drug_chronic_amt%255E%255E0%2540%2540drug_chemo_amt%255E%255E0%2540%2540device_amt%255E%255E0%2540%2540consumable_amt%255E%255E0%2540%2540device_rent_amt%255E%255E0%2540%2540terapi_konvalesen%255E%255E0%2540%2540panelitem_1011_3%255E%255E{icd10}%2540%2540panelitem_1012_1%255E%255E{icd9}%2540%2540panelitem_1011_4%255E%255E%2540%2540panelitem_1012_2%255E%255E%2540%2540jkn_sistole%255E%255E0%2540%2540jkn_diastole%255E%255E0%2540%2540jkn_apgar_1_appearance%255E%255E%2540%2540jkn_apgar_1_pulse%255E%255E%2540%2540jkn_apgar_1_grimace%255E%255E%2540%2540jkn_apgar_1_activity%255E%255E%2540%2540jkn_apgar_1_respiration%255E%255E%2540%2540jkn_apgar_5_appearance%255E%255E%2540%2540jkn_apgar_5_pulse%255E%255E%2540%2540jkn_apgar_5_grimace%255E%255E%2540%2540jkn_apgar_5_activity%255E%255E%2540%2540jkn_apgar_5_respiration%255E%255E%2540%2540jkn_usia_kehamilan%255E%255E%2540%2540jkn_gravida%255E%255E%2540%2540jkn_partus%255E%255E%2540%2540jkn_abortus%255E%255E%2540%2540jkn_onset_kontraksi%255E%255Espontan%2540%2540nomor_rujukan%255E%255E%2540%2540kode_perujuk%255E%255E%2540%2540cara_masuk%255E%255Erujukan_fktp%2540%2540usia_kehamilan%255E%255E0%2540%2540sistole%255E%255E0%2540%2540diastole%255E%255E0%2540%2540gravida%255E%255E0%2540%2540partus%255E%255E0%2540%2540abortus%255E%255E0%2540%2540onset_kontraksi%255E%255Espontan%2540%2540riwayat_sc%255E%255E0%2540%2540kuretase%255E%255E0%2540%2540nama_operasi%255E%255E%2540%2540payplan_id%255E%255E3%2540%2540cob_id%255E%255E-%2540%2540cara_masuk%255E%255Egp%2540%2540bayi_lahir_status_cd%255E%255E1%2540%2540covid19_status_cd%255E%255E4%2540%2540discharge%255E%255Ehome%2540%2540attending_doctor%255E%255E1%257C{dpjp_option}%2540%2540rs_tariff%255E%255E{rs_tarif}%2540%2540sp%255E%255ENone%2540%2540sr%255E%255ENone%2540%2540si%255E%255ENone%2540%2540sd%255E%255ENone%2540%2540anamnesa%255E%255E%2540%2540indikasi_ranap%255E%255E%2540%2540diagnosa_primer%255E%255E%2540%2540diagnosa_sekunder%255E%255E%2540%2540prosedur%255E%255E%2540%2540laporan_operasi%255E%255E'
                send2_grouping_url = f'http://grey.lerix.co.id/E-Klaim/ajaxreq.php?ac=pt&ff=app_grouper&ffargs[0]={number}&ffargs[1]=no_kartu%255E%255E{no_peserta}%2540%2540no_sep%255E%255E{no_sep}%2540%2540admission_type%255E%255E{tipe_rawat}%2540%2540tariff_class%255E%255E{kelas_rawat}%2540%2540admission_dttm%255E%255E{Tglplgsjp.year}-{Tglplgsjp.month:02}-{Tglplgsjp.day:02}%2520{sekarang.hour:02}%253A{sekarang.minute:02}%253A{sekarang.second:02}%2540%2540discharge_dttm%255E%255E{Tglplgsjp.year}-{Tglplgsjp.month:02}-{Tglplgsjp.day:02}%2520{sekarang.hour:02}%253A{sekarang.minute:02}%253A{sekarang.second:02}%2540%2540episodes%255E%255E%2540%2540cc_ind%255E%255E0%2540%2540akses_naat%255E%255EC%2540%2540isoman_ind%255E%255E0%2540%2540rs_darurat_ind%255E%255E0%2540%2540co_insidence_ind%255E%255E0%2540%2540cgrp_rs_darurat_ind%255E%255E0%2540%2540cgrp_isoman_ind%255E%255E0%2540%2540upgrade_class_los%255E%255E0%2540%2540ventilator_start_dttm%255E%255E0000-00-00%252000%253A00%253A00%2540%2540ventilator_stop_dttm%255E%255E0000-00-00%252000%253A00%253A00%2540%2540icu_los%255E%255E0%2540%2540birth_weight%255E%255E{birth_weight}%2540%2540adl1%255E%255E12%2540%2540adl2%255E%255E12%2540%2540jkn_sitb_noreg%255E%255E%2540%2540covid19_no_sep%255E%255E%2540%2540billing_amount_pex%255E%255E0%2540%2540billing_amount%255E%255E1000000%2540%2540procedure_amt%255E%255E1%252C000%252C000%2540%2540surgical_amt%255E%255E0%2540%2540consul_amt%255E%255E0%2540%2540expert_amt%255E%255E0%2540%2540nursing_amt%255E%255E0%2540%2540ancillary_amt%255E%255E0%2540%2540radiology_amt%255E%255E0%2540%2540laboratory_amt%255E%255E0%2540%2540blood_amt%255E%255E0%2540%2540rehab_amt%255E%255E0%2540%2540room_amt%255E%255E0%2540%2540intensive_amt%255E%255E0%2540%2540drug_amt%255E%255E0%2540%2540drug_chronic_amt%255E%255E0%2540%2540drug_chemo_amt%255E%255E0%2540%2540device_amt%255E%255E0%2540%2540consumable_amt%255E%255E0%2540%2540device_rent_amt%255E%255E0%2540%2540terapi_konvalesen%255E%255E0%2540%2540panelitem_1011_3%255E%255E{icd10}%2540%2540panelitem_1012_1%255E%255E{icd9}%2540%2540panelitem_1011_4%255E%255E%2540%2540panelitem_1012_2%255E%255E%2540%2540jkn_sistole%255E%255E0%2540%2540jkn_diastole%255E%255E0%2540%2540jkn_apgar_1_appearance%255E%255E%2540%2540jkn_apgar_1_pulse%255E%255E%2540%2540jkn_apgar_1_grimace%255E%255E%2540%2540jkn_apgar_1_activity%255E%255E%2540%2540jkn_apgar_1_respiration%255E%255E%2540%2540jkn_apgar_5_appearance%255E%255E%2540%2540jkn_apgar_5_pulse%255E%255E%2540%2540jkn_apgar_5_grimace%255E%255E%2540%2540jkn_apgar_5_activity%255E%255E%2540%2540jkn_apgar_5_respiration%255E%255E%2540%2540jkn_usia_kehamilan%255E%255E0%2540%2540jkn_gravida%255E%255E0%2540%2540jkn_partus%255E%255E0%2540%2540jkn_abortus%255E%255E0%2540%2540jkn_onset_kontraksi%255E%255Espontan%2540%2540nomor_rujukan%255E%255E%2540%2540kode_perujuk%255E%255E%2540%2540cara_masuk%255E%255Erujukan_fktp%2540%2540usia_kehamilan%255E%255E0%2540%2540sistole%255E%255E0%2540%2540diastole%255E%255E0%2540%2540gravida%255E%255E0%2540%2540partus%255E%255E0%2540%2540abortus%255E%255E0%2540%2540onset_kontraksi%255E%255Espontan%2540%2540riwayat_sc%255E%255E0%2540%2540kuretase%255E%255E0%2540%2540nama_operasi%255E%255E%2540%2540payplan_id%255E%255E3%2540%2540cob_id%255E%255E-%2540%2540cara_masuk%255E%255Egp%2540%2540bayi_lahir_status_cd%255E%255E1%2540%2540covid19_status_cd%255E%255E4%2540%2540discharge%255E%255Ehome%2540%2540attending_doctor%255E%255E1%257C{dpjp_option}%2540%2540rs_tariff%255E%255E{rs_tarif}%2540%2540sp%255E%255ENone%2540%2540sr%255E%255ENone%2540%2540si%255E%255ENone%2540%2540sd%255E%255ENone%2540%2540anamnesa%255E%255E%2540%2540indikasi_ranap%255E%255E%2540%2540diagnosa_primer%255E%255E%2540%2540diagnosa_sekunder%255E%255E%2540%2540prosedur%255E%255E%2540%2540laporan_operasi%255E%255E'
                send3_grouping_url = f'http://grey.lerix.co.id/E-Klaim/ajaxreq.php?ac=pt&ff=app_grouperSpecial&ffargs[0]={number}&ffargs[1]=1&ffargs[2]=sp%255E%255E{sp}%2540%2540sr%255E%255E{sr}%2540%2540si%255E%255E{si}%2540%2540sd%255E%255E{sd}'
                session.post(send1_grouping_url)
                # print(sp, sr, si, sd)
                if sp == None and sr == None and si == None and sd == None or sp == 'None' and sr == 'None' and si == 'None' and sd == 'None':
                    # print("Send 2")
                    send3_grouping_url_response = session.post(send2_grouping_url)
                else:
                    # print("Send 3")
                    send2_grouping_url_response = session.post(send2_grouping_url)
                    send3_grouping_url_response = session.post(send3_grouping_url)

                    repair_response2 = ast.literal_eval(send2_grouping_url_response.text)[1]
                    repair_response2 = repair_response2.replace("\\", "")
                    repair_response2 = str(repair_response2)
                    # print(repair_response2, "Repair Response")
                    pattern_number = r'redo_special\("(\d+)",'  # Menangkap angka di antara tanda kurung
                    match_number = re.search(pattern_number, repair_response2)
                    if match_number:
                        number_find = match_number.group(1)
                        # print(f"match_number: {number_find}")
                    # else:
                    #     print("match_number tidak ditemukan.")
                    send3_grouping_url = f'http://grey.lerix.co.id/E-Klaim/ajaxreq.php?ac=pt&ff=app_grouperSpecial&ffargs[0]={number_find}&ffargs[1]=1&ffargs[2]=sp%255E%255E{sp}%2540%2540sr%255E%255E{sr}%2540%2540si%255E%255E{si}%2540%2540sd%255E%255E{sd}'
                    send3_grouping_url_response = session.post(send3_grouping_url)
                # print(f"response3: {send3_grouping_url_response.text}")

                group_code = re.search(r"'(.*?)'", send3_grouping_url_response.text).group(1)
                nama_list = ast.literal_eval(send3_grouping_url_response.text)[-3]
                data_list = ast.literal_eval(send3_grouping_url_response.text)[1]
                data_list = data_list.replace("\\", "")
                pattern = r"Total Rp<\/td><td style='border-left:0;font-weight:bold;text-align:right;'>(.*?)<\/td>"

                match = re.search(pattern, data_list)
                if match:
                    data_list = match.group(1)
                    data_list = data_list.replace(",", "")
                    # print(f"Teks yang ditemukan: {data_list}")
                # else:
                #     print("Teks tidak ditemukan.")
                # print("Total Rp:", data_list)
                # print(type(data_list))
                # print("Kode grup:", group_code)
                # print("Nama Group:", nama_list)
                # print("Nilai dalam Rupiah:", data_list)

                repair_response = ast.literal_eval(send3_grouping_url_response.text)[1]
                repair_response = repair_response.replace("\\", "")
                repair_response = str(repair_response)
                # print(repair_response, "Repair Response")

                pattern_number = r'redo_special\("(\d+)",'  # Menangkap angka di antara tanda kurung
                match_number = re.search(pattern_number, repair_response)
                if match_number:
                    number_find = match_number.group(1)
                    # print(f"match_number: {number_find}")
                # else:
                #     print("match_number tidak ditemukan.")

                # Pola regex untuk sp
                pattern_sp = re.compile(
                    rf'name=[\'"]sp[\'"] onchange=[\'"]redo_special\("{number_find}","1",this,event\);[\'"]>(.*?)</select>',
                    re.DOTALL
                )
                data_list_match_topup_sp_pattern = re.findall(pattern_sp, repair_response)
                # print("SP Matches:", data_list_match_topup_sp_pattern)

                # Pola regex untuk sr
                pattern_sr = re.compile(
                    rf'name=[\'"]sr[\'"] onchange=[\'"]redo_special\("{number_find}","1",this,event\);[\'"]>(.*?)</select>',
                    re.DOTALL
                )

                data_list_match_topup_sr_pattern = re.findall(pattern_sr, repair_response)
                # print("SR Matches:", data_list_match_topup_sr_pattern)

                # Pola regex untuk si
                pattern_si = re.compile(
                    rf'name=[\'"]si[\'"] onchange=[\'"]redo_special\("{number_find}","1",this,event\);[\'"]>(.*?)</select>',
                    re.DOTALL
                )
                data_list_match_topup_si_pattern = re.findall(pattern_si, repair_response)
                # print("SI Matches:", data_list_match_topup_si_pattern)

                # Pola regex untuk sd
                pattern_sd = re.compile(
                    rf'name=[\'"]sd[\'"] onchange=[\'"]redo_special\("{number_find}","1",this,event\);[\'"]>(.*?)</select>',
                    re.DOTALL
                )
                # print(pattern_sd)
                data_list_match_topup_sd_pattern = re.findall(pattern_sd, repair_response)
                # print("SD Matches:", data_list_match_topup_sd_pattern)

                pasien = 'http://grey.lerix.co.id/E-Klaim/index.php?X_his=padm&slpat_selectpat=1'
                session.post(pasien)
                hapus_pasien = f'http://grey.lerix.co.id/E-Klaim/ajaxreq.php?ac=slpt&ff=app_deletePatient&ffrnd={waktusekarang}'
                session.post(hapus_pasien)
                # print('Hapus Pasien')
                # print("DOOOOONNNEEEEEEE-----------------")
                return group_code, nama_list, data_list, data_list_match_topup_sp_pattern, data_list_match_topup_sr_pattern, data_list_match_topup_si_pattern, data_list_match_topup_sd_pattern
            except Exception as e:
                # print(f"Exception: {e}")
                pasien = 'http://grey.lerix.co.id/E-Klaim/index.php?X_his=padm&slpat_selectpat=1'
                session.post(pasien)
                hapus_pasien = f'http://grey.lerix.co.id/E-Klaim/ajaxreq.php?ac=slpt&ff=app_deletePatient&ffrnd={waktusekarang}'
                session.post(hapus_pasien)
                # print('Hapus Pasien Karena Error')
        else:
            group_code = 0
            nama_list = 0
            data_list = 0
            # print("Kode grup:", group_code)
            # print("Nama Group:", nama_list)x
            # print("Nilai dalam Rupiah:", data_list)
            # print('Login failed!')
            # print(f'Response URL: {response.url}')
            # print(f'Response Content: {response.text}')
            return group_code, nama_list, data_list


def query_icd10(request):
    query = request.GET.get('query', '')
    if query:
        session = requests.Session()

        cookies = browsercookie.chrome()
        cookie_value = 'u7tqf5m6taufhqh073g6frkbo2'
        for cookie in cookies:
            if cookie.name == "XOCPSID":
                cookie_value = cookie.value
                break

        if cookie_value is None:
            raise ValueError("Cookie XOCPSID tidak ditemukan")

        url = 'http://grey.lerix.co.id/e-klaim/ajaxreq.php'
        headers = {
            'Host': '103.56.92.75',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.112 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Origin': 'http://grey.lerix.co.id',
            'Referer': f'http://grey.lerix.co.id/E-Klaim/index.php?rand={uuid.uuid4()}',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cookie': f'XOCPSID={cookie_value}',
            'Connection': 'keep-alive',
        }
        payload = {
            'ac': 'pnlejx',
            'ff': 'app_searchICD10',
            'ffargs[0]': query
        }
        response = session.post(url, headers=headers, data=payload)
        data = response.text.strip().split('\n')
        response_str = data[0]
        parsed_response = json.loads(response_str.replace("'", '"'))
        return JsonResponse(parsed_response, safe=False)
    return JsonResponse([], safe=False)


def query_icd9(request):
    query = request.GET.get('query', '')
    if query:
        session = requests.Session()

        cookies = browsercookie.chrome()
        cookie_value = 'u7tqf5m6taufhqh073g6frkbo2'
        for cookie in cookies:
            if cookie.name == "XOCPSID":
                cookie_value = cookie.value
                break

        if cookie_value is None:
            raise ValueError("Cookie XOCPSID tidak ditemukan")

        url = 'http://grey.lerix.co.id/e-klaim/ajaxreq.php'
        headers = {
            'Host': '103.56.92.75',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.112 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Origin': 'http://grey.lerix.co.id',
            'Referer': f'http://grey.lerix.co.id/E-Klaim/index.php?rand={uuid.uuid4()}',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cookie': f'XOCPSID={cookie_value}',
            'Connection': 'keep-alive',
        }
        payload = {
            'ac': 'pnlejx',
            'ff': 'app_searchICD9Proc',
            'ffargs[0]': query
        }
        response = session.post(url, headers=headers, data=payload)
        data = response.text.strip().split('\n')
        response_str = data[0]
        parsed_response = json.loads(response_str.replace("'", '"'))
        return JsonResponse(parsed_response, safe=False)
    return JsonResponse([], safe=False)


def pindahrs(koders):
    with transaction.atomic():
        session = requests.Session()

        login_url = 'http://grey.lerix.co.id/E-Klaim/login.php'

        username = 'inacbg'
        password = 'inacbg'

        hashed_password, salt = get_hash(password)

        payload = {
            'login': username,
            'rndx': hashed_password,
            'hash': 1,
            'rnd': salt
        }

        response = session.get(login_url, params=payload)
        if response.url.startswith('http://grey.lerix.co.id/E-Klaim/index.php') and 'success=1' in response.url:
            # print('Login successful!')
            # print(f'Redirected to: {response.url}')

            pindah_group = 'http://grey.lerix.co.id/E-Klaim/index.php?XP_syschpgroup_menu=0'
            session.get(pindah_group)
            setup_rs = 'http://grey.lerix.co.id/E-Klaim/index.php?XG_10=rs'
            session.get(setup_rs)

            url = 'http://grey.lerix.co.id/e-klaim/ajaxreq.php'
            payload_validate = {
                'ac': 'rsjx',
                'ff': 'app_validate',
                'ffargs[0]': f'{koders}'
            }
            response_validate_kode_rs = session.post(url=url, data=payload_validate)
            vip = "0.0"
            data = ast.literal_eval(response_validate_kode_rs.text)
            # faskes = urllib.parse.quote(data[0])
            name = urllib.parse.quote(data[1])
            province = urllib.parse.quote(data[2])
            city = urllib.parse.quote(data[3])
            address = urllib.parse.quote(data[4])
            category = urllib.parse.quote(data[5])
            type1 = urllib.parse.quote(data[6])
            type2 = urllib.parse.quote(data[7])
            code = urllib.parse.quote(data[8])
            region_code = urllib.parse.quote(data[9])
            # tariff_class_b = urllib.parse.quote(data[10])
            # tariff_class_c = urllib.parse.quote(data[11])
            unique_id = urllib.parse.quote(data[12])
            # region = urllib.parse.quote(data[13])
            # region_code_2 = urllib.parse.quote(data[14])
            tipe_tarif_pertama = data[6]
            tipe_tarif_kedua = data[7]
            # print(data[6])
            # print(data[7])
            # print(data)
            # print("-----------------------")
            # print("-----------------------")

            payload_save = {
                'ac': 'rsjx',
                'ff': 'app_save',
                'ffargs[0]': f'rs_no%5E%5E{code}%40%40rs_name%5E%5E{name}%40%40cob_company_nm%5E%5E%40%40rs_alamat%5E%5E{address}%40%40rs_kab%5E%5E{city}%40%40rs_prop%5E%5E{province}%40%40rs_class%5E%5E{category}%40%40vip_add_pct%5E%5E{vip}%40%40xtype%5E%5Efaskes%40%40rs_tariff%5E%5E{type1}%40%40rs_tariff2%5E%5E{type2}%40%40rs_reg%5E%5E{region_code}%40%40encryption_key%5E%5E{unique_id}'
                # 'ffargs[0]': 'rs_no%5E%5E7172014%40%40rs_name%5E%5ERS%20BUDI%20MULIA%20BITUNG%40%40cob_company_nm%5E%5E%40%40rs_alamat%5E%5EJL%20SAM%20RATULANGI%40%40rs_kab%5E%5EKOTA%20BITUNG%40%40rs_prop%5E%5ESULAWESI%20UTARA%40%40rs_class%5E%5EC%40%40vip_add_pct%5E%5E0.0%40%40xtype%5E%5Efaskes%40%40rs_tariff%5E%5ECS%40%40rs_tariff2%5E%5ECS%40%40rs_reg%5E%5Ereg3%40%40encryption_key%5E%5E5866161336ad8ab0249d261c2c8113ede4b58c2b9180666a5055d31f0e9fb9b1'
            }
            session.post(url=url, data=payload_save)
            # print(response_save_kode_rs.text)
            payload_update = {
                'ac': 'rsjx',
                'ff': 'app_updateKodeRS',
            }
            session.post(url=url, data=payload_update)
            session.post(url=url, data=payload_validate)
            session.post(url=url, data=payload_save)

            session.get(pindah_group)
            administrasi_klaim = 'http://grey.lerix.co.id/E-Klaim/index.php?XG_9=klaim'
            session.get(administrasi_klaim)
            # print("DONNNNEEEEE-------")
            return tipe_tarif_pertama, tipe_tarif_kedua
