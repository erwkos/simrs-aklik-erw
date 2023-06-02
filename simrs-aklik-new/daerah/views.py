from django.shortcuts import render


from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters

from .models import (
    Provinsi,
    Kabupaten,
    Kecamatan,
    Daerah
)
from .serializers import (
    KecamatanSerializer
)


class KecamatanViewSet(GenericViewSet):
    queryset = Kecamatan.objects.all()
    serializer_class = KecamatanSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nama']

    def list(self, request):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


