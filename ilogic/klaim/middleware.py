from django.db.models import Q
from django.utils.decorators import sync_and_async_middleware

from vpkaak.choices import StatusReviewChoices, StatusChoices
from vpkaak.models import RegisterPostKlaim, SamplingDataKlaimCBG
from .choices import StatusDataKlaimChoices, StatusRegisterChoices, NamaJenisKlaimChoices
from .models import DataKlaimCBG, RegisterKlaim, DataKlaimObat


class DaftarClaimCount:
    def __init__(self, get_response):
        self.get_response = get_response

    @sync_and_async_middleware
    def __call__(self, request):
        request.count_registerclaim = 0
        request.is_faskes = None
        request.is_cabang = None

        if hasattr(request.user, 'faskes_set'):
            if request.user.faskes_set.all().first():
                # user anggota faskes
                request.is_faskes = True

                obj_rs = RegisterKlaim.objects.filter(faskes=request.user.faskes_set.all().first())
                obj_data_klaim = DataKlaimCBG.objects.filter(faskes=request.user.faskes_set.all().first())
                obj_data_klaim_obat = DataKlaimObat.objects.filter(faskes=request.user.faskes_set.all().first())

                if request.user.check_permissions(group_list=['faskes']):
                    obj_rs = obj_rs.filter(
                        status=StatusRegisterChoices.DIKEMBALIKAN
                    )
                    request.count_registerclaim = obj_rs.count()

                if request.user.check_permissions(group_list=['faskes']):
                    obj_data_klaim_pending = obj_data_klaim.filter(status=StatusDataKlaimChoices.PENDING,
                                                                   prosesklaim=True)
                    obj_data_klaim_dispute = obj_data_klaim.filter(status=StatusDataKlaimChoices.DISPUTE,
                                                                   prosesklaim=True)
                    obj_data_klaim_pending_dispute = obj_data_klaim_pending.count() + obj_data_klaim_dispute.count()

                    obj_data_klaim_pending_obat = obj_data_klaim_obat.filter(status=StatusDataKlaimChoices.PENDING,
                                                                             prosesklaim=True)
                    obj_data_klaim_dispute_obat = obj_data_klaim_obat.filter(status=StatusDataKlaimChoices.DISPUTE,
                                                                             prosesklaim=True)
                    obj_data_klaim_pending_dispute_obat = obj_data_klaim_pending_obat.count() + obj_data_klaim_dispute_obat.count()

                    request.count_data_klaim = obj_data_klaim_pending_dispute
                    request.count_data_klaim_obat = obj_data_klaim_pending_dispute_obat

        if hasattr(request.user, 'kantorcabang_set'):

            if request.user.kantorcabang_set.all().first():
                # user adalah anggota kantor cabang
                request.is_cabang = True

                kode_cabang = request.user.kantorcabang_set.all().first().kode_cabang

                # object register klaim
                obj = RegisterKlaim.objects.filter(
                    nomor_register_klaim__startswith=kode_cabang
                )

                # object post klaim
                obj_register_post_klaim = RegisterPostKlaim.objects.filter(
                    user__kantorcabang=request.user.kantorcabang_set.all().first())
                obj_sampling_data_klaim_cbg = SamplingDataKlaimCBG.objects.filter(
                    register__user__kantorcabang=request.user.kantorcabang_set.all().first())

                if request.user.check_permissions(group_list=['verifikator']):
                    # register klaim verifikator
                    request.count_finalisasi = 0
                    finalisasi_reguler = obj.filter(jenis_klaim__nama=NamaJenisKlaimChoices.CBG_REGULER,
                                                    status=StatusRegisterChoices.VERIFIKASI,
                                                    verifikator=request.user,
                                                    file_data_klaim__isnull=False)

                    for i in finalisasi_reguler:
                        if i.sisa_klaim == 0:
                            request.count_finalisasi += 1

                    finalisasi_reguler_obat = obj.filter(jenis_klaim__nama=NamaJenisKlaimChoices.OBAT_REGULER,
                                                         status=StatusRegisterChoices.VERIFIKASI,
                                                         verifikator=request.user,
                                                         file_data_klaim__isnull=False)

                    for i in finalisasi_reguler_obat:
                        if i.sisa_klaim == 0:
                            request.count_finalisasi += 1

                    finalisasi_susulan = obj.filter(jenis_klaim__nama=NamaJenisKlaimChoices.CBG_SUSULAN,
                                                    status=StatusRegisterChoices.VERIFIKASI,
                                                    verifikator=request.user)

                    for i in finalisasi_susulan:
                        if i.sisa_klaim == 0:
                            request.count_finalisasi += 1

                    finalisasi_susulan_obat = obj.filter(jenis_klaim__nama=NamaJenisKlaimChoices.OBAT_SUSULAN,
                                                         status=StatusRegisterChoices.VERIFIKASI,
                                                         verifikator=request.user)

                    for i in finalisasi_susulan_obat:
                        if i.sisa_klaim == 0:
                            request.count_finalisasi += 1

                    data_claim = DataKlaimCBG.objects.filter(
                        verifikator=request.user,
                        status=StatusDataKlaimChoices.PROSES,
                        prosesklaim=False,
                    ).count()

                    request.count_dataclaim = data_claim

                    data_claim_obat = DataKlaimObat.objects.filter(
                        verifikator=request.user,
                        status=StatusDataKlaimChoices.PROSES,
                        prosesklaim=False,
                    ).count()

                    request.count_dataclaim_obat = data_claim_obat

                    obj = obj.filter(
                        status=StatusRegisterChoices.TERIMA,
                        verifikator=request.user
                    )

                    request.count_registerclaim = obj.count()

                    # register postklaim verifikator
                    obj_register_post_klaim = obj_register_post_klaim.filter(
                        status__in=[StatusChoices.Register, StatusChoices.Verifikasi],
                    )
                    request.count_register_post_klaim = obj_register_post_klaim.count()

                    # sampling data postklaim verifikator
                    obj_sampling_data_klaim_cbg = obj_sampling_data_klaim_cbg.filter(
                        status=StatusReviewChoices.Belum
                    )

                    request.count_sampling_data_klaim_cbg = obj_sampling_data_klaim_cbg.count()

                    # sampling data postklaim verifikator
                    obj_sampling_data_klaim_cbg_kp = obj_sampling_data_klaim_cbg.filter(
                        status=StatusReviewChoices.Belum, is_from_kp=True
                    )

                    request.count_sampling_data_klaim_cbg_kp = obj_sampling_data_klaim_cbg_kp.count()


                if request.user.check_permissions(group_list=['adminAK']):
                    pengajuan = obj
                    obj_terima = pengajuan.filter(Q(status=StatusRegisterChoices.TERIMA) & Q(verifikator__isnull=True))
                    obj_pengajuan = pengajuan.filter(status=StatusRegisterChoices.PENGAJUAN)
                    count_pengajuan = obj_terima.count() + obj_pengajuan.count()

                    request.count_registerclaim = count_pengajuan

                    # hitung berapa register klaim yang final belum di BOA
                    registerklaim_belum_boa = obj.filter(status=StatusRegisterChoices.SELESAI, prosesboa=False)
                    request.count_registerklaim_belum_boa = registerklaim_belum_boa.count()

                if request.user.check_permissions(group_list=['stafupk']):
                    # register postklaim stafupk
                    obj_register_post_klaim = obj_register_post_klaim.filter(
                        status__in=[StatusChoices.Register, StatusChoices.Verifikasi],
                    )
                    request.count_register_post_klaim = obj_register_post_klaim.count()

        response = self.get_response(request)
        return response
