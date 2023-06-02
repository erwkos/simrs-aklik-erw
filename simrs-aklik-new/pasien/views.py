

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters

from .models import Pasien
from .serializers import PasienSerializer


class PasienViewSet(GenericViewSet):
    queryset = Pasien.objects.all()
    serializer_class = PasienSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nama', 'nik', 'no_rekam_medis']

    def list(self, request):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
