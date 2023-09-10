
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    DataKlaimCBG
)
from .serializers import (
    MonitoringDataKlaimSerializer
)
from .permissions import (
    IsAdminAK,
    IsVerifikator
)


class MonitoringDataKlaimViewSet(GenericViewSet):
    queryset = DataKlaimCBG.objects.all()
    serializer_class = MonitoringDataKlaimSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated, IsAdminAK, IsVerifikator]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['NOSEP']
    filterset_fields = ['status', 'verifikator']

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset.filter(register_klaim__faskes__kantor_cabang=self.request.user.kantorcabang_set.first())
        return super(MonitoringDataKlaimViewSet, self).get_queryset()

    def list(self, request):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        pagination = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(pagination)
