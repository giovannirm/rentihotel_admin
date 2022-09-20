from rest_framework import viewsets,generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser

from .models import Habitacion
from .serializers import *
from utils.permission import IsUserManagment

from django.http import JsonResponse
from django.db import connection

from utils.cursor import dictfetchall


class ListRoomsByHotelView(APIView):
    pagination_class = None
    permission_classes = ([ IsUserManagment, ])  

    def get_queryset(self,pk):
        queryset = Habitacion.objects.filter(hotel=pk).order_by('numero_habitacion')
        return queryset

    def get(self ,request,pk=None,*arg, **kwargs):
        type_room = request.query_params.get('type')
        initial_date = request.query_params.get('initial_date')
        final_date = request.query_params.get('final_date')

        if type_room :
            if initial_date and final_date:
                try:
                    with connection.cursor() as cursor: 
                        cursor.callproc('fn_available_rooms_type',[ pk,type_room,initial_date,final_date])
                        data = cursor.fetchall()
                        result = dictfetchall(cursor,data) 
                        return JsonResponse(result, safe=False)
                except Exception as e:
                    return Response({ 'message': str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                rooms = self.get_queryset(pk).filter(tipo_habitacion_id=type_room)
        else:
            rooms = self.get_queryset(pk)
        serializers = ListRoomsByHotelSerializer(rooms,many=True)
        return Response(serializers.data)
        
    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        # For debugging purposes only.
        from django.db import connection
        #print(connection.queries)
        #print('# of Queries: {}'.format(len(connection.queries)))
        return response








