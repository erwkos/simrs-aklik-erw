from django.db.models import Q
from django.utils.decorators import sync_and_async_middleware

from .choices import StatusDataKlaimChoices, StatusRegisterChoices, NamaJenisKlaimChoices
from .models import DataKlaimCBG, RegisterKlaim


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

                if request.user.check_permissions(group_list=['faskes']):
                    obj_rs = obj_rs.filter(
                        status=StatusRegisterChoices.DIKEMBALIKAN
                    )
                    request.count_registerclaim = obj_rs.count()

                if request.user.check_permissions(group_list=['faskes']):
                    obj_data_klaim_pending = obj_data_klaim.filter(status=StatusDataKlaimChoices.PENDING, prosesklaim=True)
                    obj_data_klaim_dispute = obj_data_klaim.filter(status=StatusDataKlaimChoices.DISPUTE, prosesklaim=True)
                    obj_data_klaim_pending_dispute = obj_data_klaim_pending.count() + obj_data_klaim_dispute.count()

                    request.count_data_klaim = obj_data_klaim_pending_dispute

        if hasattr(request.user, 'kantorcabang_set'):

            if request.user.kantorcabang_set.all().first():
                # user adalah anggota kantor cabang
                request.is_cabang = True

                kode_cabang = request.user.kantorcabang_set.all().first().kode_cabang
                obj = RegisterKlaim.objects.filter(
                    nomor_register_klaim__startswith=kode_cabang
                )
                if request.user.check_permissions(group_list=['verifikator']):
                    request.count_finalisasi = 0
                    finalisasi_reguler = obj.filter(jenis_klaim__nama=NamaJenisKlaimChoices.CBG_REGULER,
                                                    status=StatusRegisterChoices.VERIFIKASI,
                                                    verifikator=request.user,
                                                    file_data_klaim__isnull=False)

                    for i in finalisasi_reguler:
                        if i.sisa_klaim == 0:
                            request.count_finalisasi += 1

                    finalisasi_susulan = obj.filter(jenis_klaim__nama=NamaJenisKlaimChoices.CBG_SUSULAN,
                                                    status=StatusRegisterChoices.VERIFIKASI,
                                                    verifikator=request.user)

                    for i in finalisasi_susulan:
                        if i.sisa_klaim == 0:
                            request.count_finalisasi += 1

                    data_claim = DataKlaimCBG.objects.filter(
                        verifikator=request.user,
                        status=StatusDataKlaimChoices.PROSES,
                        prosesklaim=False,
                    ).count()

                    request.count_dataclaim = data_claim

                    obj = obj.filter(
                        status=StatusRegisterChoices.TERIMA,
                        verifikator=request.user
                    )

                    request.count_registerclaim = obj.count()

                if request.user.check_permissions(group_list=['adminAK']):
                    pengajuan = obj
                    obj_terima = pengajuan.filter(Q(status=StatusRegisterChoices.TERIMA) & Q(verifikator__isnull = True))
                    obj_pengajuan = pengajuan.filter(status=StatusRegisterChoices.PENGAJUAN)
                    count_pengajuan = obj_terima.count() + obj_pengajuan.count()

                    request.count_registerclaim = count_pengajuan

        response = self.get_response(request)
        return response
