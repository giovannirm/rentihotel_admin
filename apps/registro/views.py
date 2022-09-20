from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import json
from django.http import JsonResponse
from django.db import connection

from django.http import Http404 
from .models import Registro
from hotel.models import Hotel
from .serializers import RecordSerializers, OnlyRecordSerializers , ReservationRecordSerializer

from utils.permission import IsUserManagment
from utils.cursor import dictfetchall ,dict_rooms
from utils.utils import now_date

from datetime import datetime


# --> registro + registro_habitacion  
class RecordViewSet(viewsets.ModelViewSet):
    serializer_class = RecordSerializers
    permission_classes = ([IsUserManagment])

    def get_serializer_context(self):
        return {"request": self.request }
  
    def get_queryset(self):
        try:
            obj  = Hotel.objects.get(pk=self.kwargs['pk_h'])
            records = Registro.objects.all().filter(hotel_id=self.kwargs['pk_h'])#.order_by('id')
            queryset = self.get_serializer_class().record_prefetch(records)
            #queryset = records
            return queryset
        except Hotel.DoesNotExist:
            raise Http404

    def create(self,request ,pk_h):
        serializer = RecordSerializers(data=request.data , context={'request':request})
        serializer.is_valid(raise_exception=True)
        records_room = request.data.get('registros_habitacion') 
        record = (request.data).copy()
        record.pop('registros_habitacion')
             
        try:     
            hotel = Hotel.objects.get(pk=pk_h)
            with connection.cursor() as cursor:
                cursor.callproc('fn_save_records',[str(json.dumps(record)), str(json.dumps(records_room )), pk_h, request.user.id , now_date()])
                data = cursor.fetchall()                     
                result = data[0][0] 
                return JsonResponse(result, safe=False,status=status.HTTP_201_CREATED)    
        except Hotel.DoesNotExist:
            return Response({'message': "El hotel no existe"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error = str(e).split('\n')[0].split(',')
            if error[0] == '400':
                return Response({'message': error[1]}, status=status.HTTP_400_BAD_REQUEST)            
            return Response({'message': str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        # For debugging purposes only.
        from django.db import connection
        #print(connection.queries)
        #print('# of Queries: {}'.format(len(connection.queries)))
        return response


class RoomBookingView(APIView):
    permission_classes = ([IsUserManagment])
    def get(self,request,pk_h,*args,**kwargs):
        rooms = request.GET.getlist('rooms[]')
        initial_date = request.query_params.get('initial_date')
        final_date = request.query_params.get('final_date')        
        if len(rooms)!= 0 and initial_date and final_date :      
            try:
                with connection.cursor() as cursor: 
                    rooms_availability = dict()
                    for i in range(0,len(rooms)):
                        cursor.callproc('fn_room_booking',[ pk_h,rooms[i],initial_date,final_date])
                        data = cursor.fetchall()
                        result = dictfetchall(cursor,data)
                        rooms_availability[rooms[i]] = result                    
                    return JsonResponse(rooms_availability, safe=False)
            except Exception as e:
                return Response({ 'message': str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'message':'Request could not be performed with received data'},status=status.HTTP_400_BAD_REQUEST)

class RoomBookingViewV2(APIView):
    permission_classes = ([IsUserManagment])
    def get(self,request,pk_h,*args,**kwargs):
        rooms = request.GET.getlist('rooms[]')
        rooms2= [ int(i) for i in rooms]
      
        initial_date = request.query_params.get('initial_date')
        final_date = request.query_params.get('final_date') 
        
        try:
            with connection.cursor() as cursor: 
                query = "SELECT * from fn_room_booking_multiple_json( {},'{}','{}',ARRAY {})".format(pk_h,initial_date,final_date ,rooms2)
                cursor.execute(query)
                data = cursor.fetchall()
                result = data[0][0]
                rooms_availability = dict_rooms(result , rooms2)                                   
                return JsonResponse(rooms_availability, safe=False)
        except Exception as e:
            return Response({ 'message': str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'message':'Request could not be performed with received data'},status=status.HTTP_400_BAD_REQUEST)


# solo reservas 
class RegisterReservationRecord(APIView):
    permission_classes = [(IsUserManagment)]
    def post(self,request,pk_h):
        data=request.data
        serializer = ReservationRecordSerializer(data=data , context={"request":request})
        serializer.is_valid(raise_exception=True)

        rg_id = request.data['registro_cliente']['id']
        rg_num_doc = request.data['registro_cliente']['numero_documento']
        
        records_room = request.data['registro']['registros_habitacion']
        record = (request.data['registro'] ).copy()
        record.pop('registros_habitacion')
        try:
            with connection.cursor() as cursor: 
                cursor.callproc('fn_register_rclient',[ pk_h,rg_id,rg_num_doc,request.user.id,now_date()])
                client = cursor.fetchall()
                record['cliente'] =client[0][0]               

                cursor.callproc('fn_save_records',[ str(json.dumps(record)), str(json.dumps(records_room )), pk_h, request.user.id , now_date()])
                data = cursor.fetchall()                     
                result = data[0][0] 
                return JsonResponse(result, safe=False,status=status.HTTP_201_CREATED)
                       
        except KeyError:
            return Response({'message': "El registro no existe"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            error = str(e).split('\n')[0].split(',')
            if error[0] == '404':
                return Response({'message': error[1]}, status=status.HTTP_404_NOT_FOUND)            
            return Response({'message': str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        # For debugging purposes only.
        from django.db import connection
        #print(connection.queries)
        #print('# of Queries: {}'.format(len(connection.queries)))
        return response






# -------  
class OnlyRecorViewSet(viewsets.ModelViewSet):
    serializer_class = OnlyRecordSerializers
    permission_classes = ([IsUserManagment])
   
    def get_serializer_context(self):
        return {"request": self.request }

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RecordDetailSerializers 
        if self.action == 'list':
            return RecordListSerializer
        return self.serializer_class
  
    def get_queryset(self):
        try:
            obj  = Hotel.objects.get(pk=self.kwargs['pk_h'])
            queryset = Registro.objects.all().filter(hotel_id=self.kwargs['pk_h']).order_by('id')
            #queryset = self.get_serializer_class().record_prefetch(records)
            return queryset
        except Hotel.DoesNotExist:
            raise Http404
      





   
   
    