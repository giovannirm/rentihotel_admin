from rest_framework import viewsets ,generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from django.db import connection

from .models import Reserva
from .serializers import ReservationsCustomerSerializers, ReservationSerializers ,ReservationDetailSerializers
from utils.permission import IsUserManagment
from utils.cursor import dictfetchall
from utils.utils import random_code ,now_date

import json


## MOD RESERVAS
class ReservationCustomer(generics.CreateAPIView):
    serializer_class = ReservationsCustomerSerializers
    permission_classes = ()

    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        # For debugging purposes only.
        from django.db import connection
        print(connection.queries)
        print('# of Queries: {}'.format(len(connection.queries)))
        return response

class ReservationCustomerView(APIView):
    serializer_class = ReservationsCustomerSerializers
    permission_classes = ()

    def post(self,request):
        serializer = ReservationsCustomerSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        reservations_detail = request.data.get('reserva_detalle') 
        reservation = (request.data).copy()
        reservation.pop('reserva_detalle')        
        try: 
            with connection.cursor() as cursor:
                cursor.callproc('fn_save_reservations',[str(json.dumps(reservation)), str(json.dumps(reservations_detail)),random_code(6),now_date()])
                data = cursor.fetchall()                     
                result = data[0][0] 
                return JsonResponse(result, safe=False,status=status.HTTP_201_CREATED)      
        except Exception as e:
            return Response({'message': str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        # For debugging purposes only.
        from django.db import connection
        print(connection.queries)
        print('# of Queries: {}'.format(len(connection.queries)))
        return response

## MOD - GESTION 
class ReservationViewSet(viewsets.ModelViewSet):
    permission_classes = ([ IsUserManagment, ]) 
    queryset = Reserva.objects.all().prefetch_related('reserva_detalle').select_related('registro_cliente')
    serializer_class = ReservationSerializers
            
    def get_queryset(self):
        queryset = self.queryset.filter(hotel_id=self.kwargs['pk_h']).exclude(estado_reserva='PENDIENTE').order_by('-id')
        return queryset

    def list(self, request,pk_h):
        status = request.query_params.get('status')   
        try:
            with connection.cursor() as cursor:
                cursor.callproc('fn_list_reservations',[pk_h,str(status)])
                data = cursor.fetchall()                      
                result = dictfetchall(cursor,data)
                return JsonResponse(result, safe=False)
        except Exception as e:
            error = str(e).split('\n')[0].split(',')
            if error[0] == '404':
                return Response({'message': error[1]}, status=404)            
            return Response({'message': str(e) }, status=500)
        
        '''     
        if status :
            queryset = self.get_queryset().filter(estado_reserva__istartswith=status)
        else:
            queryset = self.get_queryset()        
        serializer = ReservationSerializers(queryset, many=True)
        return Response(serializer.data)
        '''
    
    def retrieve(self, request,pk_h,pk):
        try:
            with connection.cursor() as cursor:
                cursor.callproc('fn_detail_reservation',[pk_h,pk])
                data = cursor.fetchall()                      
                result = data[0][0]
                return JsonResponse(result, safe=False)
        except Exception as e:
            error = str(e).split('\n')[0].split(',')
            if error[0] == '404':
                return Response({'message': error[1]}, status=404)            
            return Response({'message': str(e) }, status=500)
    
    def update(self, request,pk_h,pk):
        try:
            reserva = Reserva.objects.get(pk=pk,hotel_id=pk_h)
            with connection.cursor() as cursor: 
                query = "UPDATE reserva_reserva SET estado_reserva='CANCELADO' WHERE id={} and hotel_id={}".format(pk,pk_h)
                cursor.execute(query)                                   
                return Response({ 'message':'Se cancelo reserva' },status=status.HTTP_200_OK)
        except Reserva.DoesNotExist:
            return Response({'message': "La reserva no existe"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({ 'message': str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        # For debugging purposes only.
        from django.db import connection
        print(connection.queries)
        print('# of Queries: {}'.format(len(connection.queries)))
        return response
