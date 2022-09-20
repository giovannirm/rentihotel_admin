from rest_framework import viewsets,generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404 

from tipohabitacion.models import TipoHabitacion
from utils.permission import IsUserManagment
from .models import Tiempo
from .serializers import  *


class TimeSelectView(generics.ListAPIView):
    pagination_class = None
    permission_classes = ([IsUserManagment])
    serializer_class = TimeSelectSerializers
    queryset = Tiempo.objects.all()

    def get_queryset(self):
        try:
            type_room = TipoHabitacion.objects.get(pk=self.kwargs['pk_tr'],hotel=self.kwargs['pk_h'])
            queryset = self.queryset.filter(tipo_habitacion=self.kwargs['pk_tr'],tipo_habitacion__hotel=self.kwargs['pk_h'])
            return queryset
        except TipoHabitacion.DoesNotExist:
           raise Http404("Tipo Habitacion no existe")
