import re
from django.http import Http404
from django.http import JsonResponse
from django.db import connection

from rest_framework import generics,viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser

from utils.permission import  IsOwner,IsAdmin,IsOwnerOrAdmin
from utils.cursor import dictfetchall,dict_rooms_availability
from utils.permission import IsUserManagment
from .models import Hotel
from .serializers import *
from usuario.models import User

## MOD - RESERVAS
#falta paginacion!!!!
class SearchHotelsByPlace(APIView):
    permission_classes = () 
    def get(self, request ,format=None ):
        word = request.query_params.get('words')
        if word:            
            try:            
            #cursor = connection.cursor()
                with connection.cursor() as cursor:
                    cursor.callproc('fn_search_place',[word,])
                    data = cursor.fetchall()                      
                    result = dictfetchall(cursor,data)
                    return JsonResponse(result, safe=False)
            except Exception as e:
                    return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        
        return Response({ 'message': 'Request could not be performed with received data.'}, status=status.HTTP_400_BAD_REQUEST) 
    
    def post(self, request, format=None):
        p_id = request.data.get('id_busqueda') 
        fecha_ini = request.data.get('fecha_ini')
        fecha_fin = request.data.get('fecha_fin')
        p_huespedes = request.data.get('n_huespedes')
        p_campo = request.data.get('nombre_campo')
        p_departamento = request.data.get('departamento')
    
        if p_id and fecha_ini and fecha_fin and p_campo and p_departamento and p_huespedes:
            try:
                with connection.cursor() as cursor:        
                    cursor.callproc('fn_search_hotel_dates',[p_id,fecha_ini,fecha_fin,p_huespedes,p_campo,p_departamento])
                    data = cursor.fetchall()  
                    result = dictfetchall(cursor,data) 
                    serializer = HotelSearchListSerializer(result,many=True)
                return Response(serializer.data) 
            except Exception as e:
                return Response({ 'message': str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({ 'message': 'Request could not be performed with received data.'},status=status.HTTP_400_BAD_REQUEST)

class HotelsViewSet(viewsets.ModelViewSet):
    permission_classes = ()
    serializer_class = HotelDetailSerializer
    queryset = Hotel.objects.all()
    
    def get_queryset(self):
        hotels  = Hotel.objects.all()
        queryset = self.serializer_class().hotel_prefetch(hotels)
        return queryset
 
    def get_object(self, pk):
        try:
            return self.get_queryset().get(pk=pk)
        except Hotel.DoesNotExist:
            raise Http404
        
    def list(self,request):
        id_department= request.query_params.get('department')
        if id_department:
            try:            
                with connection.cursor() as cursor:
                    cursor.callproc('fn_hotels_by_department',[id_department,])
                    data = cursor.fetchall()       
                    result = dictfetchall(cursor,data)
                    return JsonResponse(result, safe=False)
            except Exception as e:
                    return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
        queryset = HotelListSerializer.hotel_prefetch(self.queryset)
        serializer = HotelListSerializer(queryset,many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        initial_date = request.query_params.get('initial_date')
        final_date = request.query_params.get('final_date')

        hotel = self.get_object(pk)
        serializer = HotelDetailSerializer(hotel) 
        data = serializer.data

        if initial_date and final_date :
            try :
                with connection.cursor() as cursor:
                    cursor.callproc('fn_available_count_rooms_type',[pk,initial_date,final_date])
                    type_available = cursor.fetchall()
                    result = dict_rooms_availability(cursor,type_available)
                    
                    type_rooms = data['tipo_habitacion']  
                    for type_room in type_rooms:
                        try:
                            type_room['disponibilidad'] = result[type_room['id']]
                        except :
                            type_room['disponibilidad'] = 0
                    return Response(data)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data)
        
    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        # For debugging purposes only.
        from django.db import connection
        print(connection.queries)
        print('# of Queries: {}'.format(len(connection.queries)))
        return response
    
    





## MOD - GESTION
class UserHotelsView(APIView):
    permission_classes = ([IsUserManagment,])
    def get(self,request,pk):
        hotel = Hotel.objects.filter(usuarios__pk=pk)
        serializer = HotelGestionSerializer(hotel,many=True)
        return Response(serializer.data)
  
