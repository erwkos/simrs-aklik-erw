from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView
from django.db import transaction
from django.db.models import Q

from datetime import datetime

from antrian.models import Antrian
from pasien.choices import StatusLayananChoices
from pasien.models import Pendaftaran


class AntrianDokterRawatJalanView(ListView):
    queryset = Antrian.objects.filter(antrian_tanggal=datetime.now()).filter(
        Q(task_id=3) | Q(task_id=4)
    )
    template_name = 'dokter/antrian-dokter.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {
            'antrian_list': self.get_queryset()
        }
        return context


class SelesaiLayananView(UpdateView):
    queryset = Antrian.objects.all()
    pk_url_kwarg = 'pk'

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        obj = self.get_object(self.get_queryset())
        obj.task_id = 4.5
        obj.save()
        obj.pendaftaran.status_layanan = StatusLayananChoices.SELESAI
        obj.pendaftaran.save()
        return redirect('/user/dashboard')

