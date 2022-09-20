from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404 

from .models import RegistroHabitacion
from .serializers import RoomRegisterDetailSerializers ,CompleteRoomRecordSerializers
from utils.permission import IsUserManagment
from registro.models import Registro





## todos los registros habitacion de un registro de un hotel 
class RecordRoomViewSet(viewsets.ModelViewSet):
    permission_classes = ([IsUserManagment])   
    serializer_class = CompleteRoomRecordSerializers
      
    def get_serializer_context(self):
        return {"request": self.request }

    def get_queryset(self):
        try:
            record  = Registro.objects.get(pk=self.kwargs['pk_r'])
            queryset = RegistroHabitacion.objects.all().filter(registro=self.kwargs['pk_r']).order_by('id')
            return queryset
        except Registro.DoesNotExist:
            raise Http404("Record does not exist")

## todos los registros habiatcion de un hotel 
class RecordRoomHotelViewSet(viewsets.ModelViewSet):
    permission_classes = ([IsUserManagment])
    queryset = RegistroHabitacion.objects.all().order_by('id')
    serializer_class = CompleteRoomRecordSerializers
    
    def get_serializer_context(self):
        return {"request": self.request }




