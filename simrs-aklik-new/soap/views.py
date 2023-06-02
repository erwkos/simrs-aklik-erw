from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, CreateView, TemplateView

from antrian.models import Antrian
from .models import (
    Subjective,
    Objective,
    Planning,
    AssessmentICD10,
    AssessmentICD9
)
from radiologi.models import (
    KategoriLayananRadiologi,
    LayananRadiologi,
    LayananRadiologiPasien
)
from lab.models import (
    LayananLab,
    LayananLabPasien,
    KategoriLayananLab
)
from otherlayanan.models import (
    LayananTindakan,
    LayananKonsultasi,
    LayananMonitoring,
    LayananEdukasi,

    LayananEdukasiPasien,
    LayananTindakanPasien,
    LayananKonsultasiPasien,
    LayananMonitoringPasien
)
from farmasi.models import (
    Obat,
    ObatPasien
)
from icd.models import (
    ICD10,
    ICD9
)
from inventory.models import (
    AlatKesehatan,
    AlatKesehatanPasien
)


class SOAPRawatJalanView(DetailView):
    queryset = Antrian.objects.all()
    template_name = 'soap/rawat-jalan/form-soap.html'
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        antrian = self.get_object(self.get_queryset())
        return {
            'antrian': antrian,
            'pasien': antrian.pendaftaran.pasien,
            'subjective': Subjective.objects.filter(antrian=antrian).first(),
            'objective': Objective.objects.filter(antrian=antrian).first(),
            'planning': Planning.objects.filter(antrian=antrian).first(),
            'layanan_radiologi': LayananRadiologi.objects.all(),
            'layanan_radiologi_pasien': LayananRadiologiPasien.objects.filter(antrian=antrian),
            'layanan_lab': LayananLab.objects.all(),
            'layanan_lab_pasien': LayananLabPasien.objects.filter(antrian=antrian),
            'kategori_layanan_lab': KategoriLayananLab.objects.all(),
            'kategori_layanan_radiologi': KategoriLayananRadiologi.objects.all(),

            'layanan_tindakan': LayananTindakan.objects.all(),
            'layanan_edukasi': LayananEdukasi.objects.all(),
            'layanan_monitoring': LayananMonitoring.objects.all(),
            'layanan_konsultasi': LayananKonsultasi.objects.all(),

            'layanan_tindakan_pasien': LayananTindakanPasien.objects.filter(antrian=antrian),
            'layanan_edukasi_pasien': LayananEdukasiPasien.objects.filter(antrian=antrian),
            'layanan_monitoring_pasien': LayananMonitoringPasien.objects.filter(antrian=antrian),
            'layanan_konsultasi_pasien': LayananKonsultasiPasien.objects.filter(antrian=antrian),

            'obat_list': Obat.objects.all(),
            'obat_pasien': ObatPasien.objects.filter(antrian=antrian),

            'icd10_list': ICD10.objects.all(),
            'icd9_list': ICD9.objects.all(),
            'assessment_icd10': AssessmentICD10.objects.filter(antrian=antrian),
            'assessment_icd9': AssessmentICD9.objects.filter(antrian=antrian),

            'alat_kesehatan': AlatKesehatan.objects.all(),
            'alat_kesehatan_pasien': AlatKesehatanPasien.objects.filter(antrian=antrian)
        }


class SubjectiveRawatJalanView(CreateView):
    queryset = Subjective.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        antrian = get_object_or_404(Antrian, id=data.get('antrian_id'))
        obj = Subjective.objects.filter(antrian=antrian)
        data.pop('antrian_id')
        data.pop('csrfmiddlewaretoken')
        data = dict(data)
        if obj.exists():
            kwargs = {key: data.get(key)[0] for key in data.keys()}
            obj.update(**kwargs)
        else:
            resume_medis = antrian.pendaftaran.resume_medis
            dokter = request.user
            kwargs = {key: data.get(key)[0] for key in data.keys()}
            kwargs['antrian'] = antrian
            kwargs['resume_medis'] = resume_medis
            kwargs['dokter'] = dokter
            Subjective.objects.create(
                **kwargs
            )
        referer = request.headers.get('Referer')
        return redirect(referer)


class ObjectiveRawatJalanView(CreateView):
    queryset = Objective.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        antrian = get_object_or_404(Antrian, id=data.get('antrian_id'))
        obj = Objective.objects.filter(antrian=antrian)
        data.pop('antrian_id')
        data.pop('csrfmiddlewaretoken')
        data = dict(data)
        if obj.exists():
            kwargs = {key: data.get(key)[0] for key in data.keys()}
            obj.update(**kwargs)
        else:
            resume_medis = antrian.pendaftaran.resume_medis
            dokter = request.user
            kwargs = {key: data.get(key)[0] for key in data.keys()}
            kwargs['antrian'] = antrian
            kwargs['resume_medis'] = resume_medis
            kwargs['dokter'] = dokter
            Objective.objects.create(
                **kwargs
            )
        referer = request.headers.get('Referer')
        return redirect(referer)


class PlanningRawatJalanView(CreateView):
    queryset = Planning.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        antrian = get_object_or_404(Antrian, id=data.get('antrian_id'))
        obj = Planning.objects.filter(antrian=antrian)
        data.pop('antrian_id')
        data.pop('csrfmiddlewaretoken')
        data = dict(data)
        if obj.exists():
            kwargs = {key: data.get(key)[0] for key in data.keys()}
            obj.update(**kwargs)
        else:
            resume_medis = antrian.pendaftaran.resume_medis
            dokter = request.user
            kwargs = {key: data.get(key)[0] for key in data.keys()}
            kwargs['antrian'] = antrian
            kwargs['resume_medis'] = resume_medis
            kwargs['dokter'] = dokter
            Planning.objects.create(
                **kwargs
            )
        referer = request.headers.get('Referer')
        return redirect(referer)


class AssessmentICD10RawatJalanView(CreateView):
    queryset = AssessmentICD10.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.POST
        antrian = get_object_or_404(Antrian, id=data.get('antrian_id'))
        icd10 = get_object_or_404(ICD10, kode=data.get('kode'))
        AssessmentICD10.objects.create(
            antrian=antrian,
            resume_medis=antrian.pendaftaran.resume_medis,
            dokter=request.user,
            nama=icd10.nama,
            kode=icd10.kode,
            icd10=icd10
        )
        referer = request.headers.get('Referer')
        return redirect(referer)


class HapusAssessmentICD10(CreateView):
    queryset = AssessmentICD10.objects.all()
    pk_url_kwarg = 'pk'

    def post(self, request, *args, **kwargs):
        obj = self.get_object(self.get_queryset())
        obj.delete()
        referer = request.headers.get('Referer')
        return redirect(referer)


class AssessmentICD9RawatJalanView(CreateView):
    queryset = AssessmentICD10.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.POST
        antrian = get_object_or_404(Antrian, id=data.get('antrian_id'))
        icd9 = get_object_or_404(ICD9, kode=data.get('kode'))
        AssessmentICD9.objects.create(
            antrian=antrian,
            resume_medis=antrian.pendaftaran.resume_medis,
            dokter=request.user,
            nama=icd9.nama,
            kode=icd9.kode,
            icd9=icd9
        )
        referer = request.headers.get('Referer')
        return redirect(referer)


class HapusAssessmentICD9(CreateView):
    queryset = AssessmentICD9.objects.all()
    pk_url_kwarg = 'pk'

    def post(self, request, *args, **kwargs):
        obj = self.get_object(self.get_queryset())
        obj.delete()
        referer = request.headers.get('Referer')
        return redirect(referer)


class RawatInapView(TemplateView):
    template_name = 'soap/rawat-inap/soap.html'
