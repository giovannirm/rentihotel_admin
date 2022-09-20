from rest_framework import viewsets
from rest_framework import generics
from .models import Distrito
from .serializers import DistritoSerializer
from rest_framework.permissions import IsAuthenticated

class DistritoViewSet(viewsets.ModelViewSet):
    queryset = Distrito.objects.all()
    serializer_class = DistritoSerializer

class ListaDistrito(generics.ListAPIView):
    pagination_class = None
    permission_classes = ()
    serializer_class = DistritoSerializer

    def get_queryset(self):
        queryset =Distrito.objects.filter(provincia=self.kwargs["pk"]).order_by('id')
        return queryset
