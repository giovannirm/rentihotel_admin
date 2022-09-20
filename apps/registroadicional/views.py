from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404 

from .models import RegistroAdicional
from .serializers import *
from registrohabitacion.models import RegistroHabitacion
from utils.permission import IsUserManagment
from adicional.models import Adicional

from django.db import connection
import json
from utils.cursor import dictfetchall
from django.http import JsonResponse

class RegisterGroupAdditionalByRoom(APIView):
    permission_classes = ([ IsUserManagment, ]) 
    serializer_class = RegisterAdditionalSerializers
     
    def get(self, request, pk_h=None,pk_r=None,format=None):     
        try: 
            record_room = RegistroHabitacion.objects.get(pk=pk_r,registro__hotel_id=pk_h) 
            with connection.cursor() as cursor:
                cursor.callproc('fn_list_register_additionals',[pk_r])
                data = cursor.fetchall()    
                result = dictfetchall(cursor,data)
                return JsonResponse(result, safe=False)
        except RegistroHabitacion.DoesNotExist:
            return Response({'message': "El registro no existe"}, status=status.HTTP_400_BAD_REQUEST)        
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
      

        #return JsonResponse(room_additionals, safe=False)        

    def post(self, request, pk_h=None,pk_r=None,format=None):
        room_additionals = RegisterAdditionalSerializers(data=request.data,many=True)
        room_additionals.is_valid(raise_exception=True)
        try: 
            record_room = RegistroHabitacion.objects.get(pk=pk_r,registro__hotel_id=pk_h)            
            with connection.cursor() as cursor:
                cursor.callproc('fn_insert_additionals',[str(json.dumps(request.data)),pk_h,pk_r])
                data = cursor.fetchall()                     
                result = data[0][0] 
                return JsonResponse(result, safe=False,status=status.HTTP_201_CREATED)        
        except RegistroHabitacion.DoesNotExist:
            return Response({'message': "El registro no existe"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error = str(e).split('\n')[0].split(',')
            if error[0] == '400':
                return Response({'message': error[1]}, status=status.HTTP_400_BAD_REQUEST)            
            return Response({'message': str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk_h=None,pk_r=None,format=None):
        room_additionals = RegisterAdditionalSerializers(data=request.data,many=True)
        room_additionals.is_valid(raise_exception=True)
        try: 
            record_room = RegistroHabitacion.objects.get(pk=pk_r,registro__hotel_id=pk_h)            
            with connection.cursor() as cursor:
                cursor.callproc('fn_update_additionals',[str(json.dumps(request.data)),pk_h,pk_r])
                data = cursor.fetchall()                     
                result = data[0][0] 
                return JsonResponse(result, safe=False)        
        except RegistroHabitacion.DoesNotExist:
            return Response({'message': "El registro no existe"}, status=status.HTTP_400_BAD_REQUEST)
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















'''
class DetailGroupAdditionalByRoom(APIView):
    permission_classes = ([ IsUserManagment, ]) 

    def get_queryset(self):
        try:
            room_record = RegistroHabitacion.objects.get(pk=self.kwargs['pk_r'],registro__hotel=self.kwargs['pk_h'])
            additionals = RegistroAdicional.objects.filter(
                registro_habitacion=self.kwargs['pk_r'],
                registro_habitacion__registro__hotel=self.kwargs['pk_h']
            )      
            return additionals
        except RegistroHabitacion.DoesNotExist:
           raise Http404("Registro Habitacion no existe")
'''
'''
    def get_queryset(self,pk_h,pk_r):
        query = f'SELECT * FROM registroadicional_registroadicional WHERE registro_habitacion_id = {pk_r}'
        try:            
            with connection.cursor() as cursor:
                cursor.execute(query)
                data = cursor.fetchall()       
                result = dictfetchall(cursor,data)                
                return result
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
'''

