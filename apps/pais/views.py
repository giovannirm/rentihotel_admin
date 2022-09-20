from rest_framework import viewsets ,generics
from .models import Pais
from .serializers import PaisSerializer
from rest_framework.response import Response
from django.http import Http404

from rest_framework.permissions import IsAuthenticated
from utils.permission import *
from rest_framework.permissions import DjangoModelPermissions

## MOD - RESERVA

class ListaPaisesView(generics.ListAPIView):
    pagination_class = None
    permission_classes = ()    
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer

    def list(self, request):
        nombre =  request.query_params.get('nombre')
        if nombre:
            try:
                queryset = Pais.objects.get(nombre__istartswith=nombre)
                serializer = PaisSerializer(queryset)
            except Pais.DoesNotExist:
                raise Http404
        else:
            queryset = self.get_queryset()
            serializer = PaisSerializer(queryset, many=True)
        return Response(serializer.data)



## MOD - GESTION 

class PaisViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer
    permission_classes = ([IsAuthenticated,])

    #permission_classes = ([CustomDjangoModelPermissions])

    def list(self, request, *args, **kwargs):
        self.queryset = Pais.objects.order_by('id')        
        return super(PaisViewSet, self).list(request, *args, **kwargs)    
    
    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = []
        return super(PaisViewSet, self).get_permissions()

