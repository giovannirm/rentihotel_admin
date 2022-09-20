from rest_framework import status
from rest_framework import generics,viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404 

from tipohabitacion.models import TipoHabitacion
from utils.permission import IsUserManagment
from hotel.models import Hotel
from .serializers import * 


## MOD RESERVAS
class TypeView(generics.ListAPIView):
    pagination_class = None
    permission_classes=()   
    serializer_class = TypeOfRoomDetailSerializer
    queryset = TipoHabitacion.objects.all()
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.get_serializer_class().room_type_prefetch(queryset) 
        return queryset
    
    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        # For debugging purposes only.
        from django.db import connection
        print(connection.queries)
        print('---------------------------------------')
        print('# of Queries: {}'.format(len(connection.queries)))
        return response

 
## MOD GESTION 

class TypeRoomSelectView(generics.ListAPIView):
    pagination_class = None
    permission_classes = ([IsUserManagment])
    serializer_class = TypeRoomSelectSerializer
    queryset = TipoHabitacion.objects.all()

    def get_queryset(self):
        queryset = self.queryset.filter(hotel=self.kwargs['pk'])
        return queryset

    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        # For debugging purposes only.
        from django.db import connection
        print(connection.queries)
        print('# of Queries: {}'.format(len(connection.queries)))
        return response


    
