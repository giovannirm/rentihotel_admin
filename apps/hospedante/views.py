from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404 

from hotel.models import Hotel
from registro.models import Registro
from registrohabitacion.models import RegistroHabitacion

from .models import Hospedante
from .serializers import HostSerializers ,HostRegisterRoomSerializers , HospedanteSerializers
from utils.permission import IsUserManagment

class HostSearchByHotel(APIView):
    permission_classes = ([ IsUserManagment, ])
    def get_queryset(self,pk):
        queryset = Hospedante.objects.all().filter(registrohabitacion__registro__hotel_id=pk).order_by('id').distinct()
        return queryset

    def post(self ,request,pk=None,*arg, **kwargs):
        numero_documento = request.data.get('numero_documento')
        tipo_documento = request.data.get('tipo_documento')
        if numero_documento and tipo_documento:  
            hosts = self.get_queryset(pk).filter(numero_documento=numero_documento,tipo_documento=tipo_documento)
            serializers = HostSerializers(hosts,many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)            
        return Response({ 'message': 'Request could not be performed with received data.'}, status=status.HTTP_400_BAD_REQUEST) 
       
    
class HostRegisterRoomViewSet(viewsets.ModelViewSet):
    pagination_class= None
    serializer_class = HostRegisterRoomSerializers
    permission_classes = ([ IsUserManagment, ]) 
         
    def get_serializer_context(self):
        return {"request": self.request }

    def get_queryset(self):
        try:                 
            record_room = RegistroHabitacion.objects.get(pk=self.kwargs['pk_r'],registro__hotel_id=self.kwargs['pk_h'])
            queryset = Hospedante.objects.all().filter(
                registrohabitacion__registro__hotel_id=self.kwargs['pk_h'],
                registrohabitacion__id=self.kwargs['pk_r']
             ).distinct()
            return queryset
        except RegistroHabitacion.DoesNotExist:
            raise Http404
 
    def create(self, request,pk_h,pk_r):
        serializer = HostRegisterRoomSerializers(data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        
        if request.data.get('id'):
            try: 
                host = Hospedante.objects.all().filter(registrohabitacion__registro__hotel_id=pk_h).distinct().get(pk=request.data.get('id')) 
                update_host = HostRegisterRoomSerializers(host, data=request.data, context={'request': self.request})
                update_host.is_valid(raise_exception=True)
                update_host.save()
                record_room = RegistroHabitacion.objects.get(pk=pk_r,registro__hotel_id=pk_h)
                record_room.hospedantes.add(host)    
                return Response(update_host.data,status=status.HTTP_201_CREATED)
            except Hospedante.DoesNotExist:
                return Response({ 'message':'Host not found to update.'}, status=status.HTTP_404_NOT_FOUND)
            except RegistroHabitacion.DoesNotExist:
                return Response({ 'message':'Record Room not found to update.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer.save() 
            return Response(serializer.data,status=status.HTTP_201_CREATED)



    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        # For debugging purposes only.
        from django.db import connection
        #print(connection.queries)
        #print('# of Queries: {}'.format(len(connection.queries)))
        return response


class HostByHotelViewSet(viewsets.ModelViewSet):
    serializer_class = HospedanteSerializers
    permission_classes = ([ IsUserManagment, ])  
        
    def get_serializer_context(self):
        return {"request": self.request }

    def get_queryset(self):
        queryset = Hospedante.objects.all().filter(registrohabitacion__registro__hotel_id=self.kwargs['pk_h']).order_by('id').distinct()
        return queryset
    
    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        # For debugging purposes only.
        from django.db import connection
        #print(connection.queries)
        #print('# of Queries: {}'.format(len(connection.queries)))
        return response 




















'''
#path('hosts', host_create, name='host_create'),
#path('hosts/<int:pk>', host_actions, name='host_actions'),

class HostViewSetV1(viewsets.ModelViewSet):
    paginator = None
    queryset = Hospedante.objects.all()
    serializer_class = HostSerializers

    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        # For debugging purposes only.
        from django.db import connection
        print(connection.queries)
        print('# of Queries: {}'.format(len(connection.queries)))
        return response 
'''