# from django.shortcuts import render
#
# from rest_framework.viewsets import GenericViewSet
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework import filters
#
#
# from .models import (
#     ICDX,
#     ICD9
# )
#
# from .serializers import (
#     ICDXSerializer,
#     ICD9Serializer
# )
#
#
# class ICFXViewSet(GenericViewSet):
#     queryset = ICDX.objects.all()
#     serializer_class = ICDXSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['nama', 'kode']
#
#     def list(self, request):
#         serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# class ICF9ViewSet(GenericViewSet):
#     queryset = ICD9.objects.all()
#     serializer_class = ICD9Serializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['nama', 'kode']
#
#     def list(self, request):
#         serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
