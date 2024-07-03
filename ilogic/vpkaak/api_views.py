from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination

from django_filters.rest_framework import DjangoFilterBackend

from vpkaak.choices import JenisAuditChoices, StatusChoices
from vpkaak.models import RegisterPostKlaim
from vpkaak.serializers import RegisterPostKlaimSerializer, RegisterPostKlaimSupervisorKPSerializer


class RegisterPostKlaimViewSet(GenericViewSet):
    # list_jenis_audit = [JenisAuditChoices.AAK, JenisAuditChoices.VPK]
    status = [StatusChoices.Register, StatusChoices.Verifikasi]
    queryset = RegisterPostKlaim.objects.filter(status__in=status).order_by('-created_at')
    serializer_class = RegisterPostKlaimSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['nomor_register', 'status', 'jenis_audit']

    def get_queryset(self):
        if self.action == 'list':
            queryset_kc = self.queryset.filter(
                user__kantorcabang=self.request.user.kantorcabang_set.all().first(), is_kp=False)
            return queryset_kc  # filter(Q(file_data_klaim=None) | Q(file_data_klaim=''))
        return super(RegisterPostKlaimViewSet, self).get_queryset()

    def list(self, request):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        pagination = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(pagination)


class RegisterPostKlaimSupervisorKPViewSet(GenericViewSet):
    status = [StatusChoices.Register, StatusChoices.Verifikasi]
    queryset = RegisterPostKlaim.objects.filter(status__in=status).order_by('-created_at')
    serializer_class = RegisterPostKlaimSupervisorKPSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['nomor_register', 'status', 'jenis_audit']

    def get_queryset(self):
        if self.action == 'list':
            queryset = self.queryset.filter(is_kp=True)
            return queryset
        return super(RegisterPostKlaimSupervisorKPViewSet, self).get_queryset()

    def list(self, request):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        pagination = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(pagination)
