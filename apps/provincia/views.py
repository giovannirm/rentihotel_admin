from rest_framework import viewsets
from rest_framework import generics
from .models import Provincia
from .serializers import ProvinciaSerializer
from rest_framework.permissions import IsAuthenticated

class ProvinciaViewSet(viewsets.ModelViewSet):
    queryset = Provincia.objects.all()
    serializer_class = ProvinciaSerializer

class ListProvincia(generics.ListAPIView):
    pagination_class = None
    permission_classes = ()
    serializer_class = ProvinciaSerializer

    def get_queryset(self):
        queryset =Provincia.objects.filter(departamento=self.kwargs["pk"])
        return queryset
