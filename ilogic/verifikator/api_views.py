from django.db.models import Q
from django.shortcuts import get_object_or_404


from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination

from django_filters.rest_framework import DjangoFilterBackend

from klaim.models import (
    RegisterKlaim,
    DataKlaimCBG
)
from klaim.choices import (
    StatusRegisterChoices, NamaJenisKlaimChoices
)
from .serializers import (
    RegisterKlaimSerializer,
    DataKlaimSerializer,
    VerifikatorSerializer
)
from user.models import User


class RegisterKlaimViewSet(GenericViewSet):
    list_jenis_klaim = [NamaJenisKlaimChoices.CBG_REGULER, NamaJenisKlaimChoices.CBG_SUSULAN]
    queryset = RegisterKlaim.objects.filter(status=StatusRegisterChoices.VERIFIKASI, jenis_klaim__nama__in=list_jenis_klaim).order_by('-tgl_aju')
    serializer_class = RegisterKlaimSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['faskes__kode_ppk', 'faskes__nama', 'nomor_register_klaim']
    
    def get_queryset(self):
        if self.action == 'list':
            queryset_kc = self.queryset.filter(nomor_register_klaim__startswith=self.request.user.kantorcabang_set.all().first().kode_cabang)
            return queryset_kc  # filter(Q(file_data_klaim=None) | Q(file_data_klaim=''))
        return super(RegisterKlaimViewSet, self).get_queryset()

    def list(self, request):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        pagination = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(pagination)


class DataKlaimViewSet(GenericViewSet):
    queryset = DataKlaimCBG.objects.all()
    serializer_class = DataKlaimSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['NOSEP']
    filterset_fields = ['status']
    
    def get_queryset(self):
        if self.action == 'list':
            return self.queryset.filter(verifikator=self.request.user, prosesklaim=False)
        return super(DataKlaimViewSet, self).get_queryset()
    
    def list(self, request):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        pagination = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(pagination)


class VerifikatorViewSet(GenericViewSet, ListModelMixin):
    queryset = User.objects.filter(groups__name='verifikator')
    serializer_class = VerifikatorSerializer

    def get_queryset(self):
        if self.action == 'list':
            register = get_object_or_404(RegisterKlaim, nomor_register_klaim=self.request.query_params.get('register'))
            verifikator = register.faskes.kantor_cabang.user.filter(groups__name='verifikator')
            return verifikator
        return super().get_queryset()

