from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404 

from .models import Adicional
from .serializers import AdditionalSerializers, AdditionalSearchSerializers

from hotel.models import Hotel
from utils.permission import IsUserManagment

from django.http import JsonResponse
from django.db import connection
from utils.cursor import dictfetchall

class AdditionalViewSet(viewsets.ModelViewSet):
    permission_classes = ([ IsUserManagment, ])  
    serializer_class = AdditionalSerializers

    def get_serializer_context(self):
        return { "request": self.request }
    
    def get_queryset(self):
        try:
            hotel = Hotel.objects.get(pk=self.kwargs['pk_h'])  
            queryset = Adicional.objects.all().filter(hotel_id=self.kwargs['pk_h']).order_by('id')
            return queryset          
        except Hotel.DoesNotExist:
            raise Http404("El hotel no existe")
    
    def get_object(self):
        queryset = self.get_queryset()
        try:
            obj = queryset.get(pk=self.kwargs['pk'])
            return obj
        except Adicional.DoesNotExist:
            raise Http404
    
    def list(self, request ,pk_h):
        additional = request.query_params.get('name')
        if additional:                      
            try:
                with connection.cursor() as cursor: 
                    cursor.callproc('fn_search_additionals',[ pk_h,additional])
                    data = cursor.fetchall()
                    result = dictfetchall(cursor,data)
                    return JsonResponse(result, safe=False)              
            except Exception as e:
                error = str(e).split('\n')[0].split(',')
                if error[0] == '404':
                    return Response({'message': error[1]}, status=status.HTTP_404_NOT_FOUND)            
                return Response({'message': str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        queryset = self.get_queryset()
        serializer = AdditionalSerializers(queryset, many=True)
        return Response(serializer.data)
    
    '''
    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        # For debugging purposes only.
        from django.db import connection
        print(connection.queries)
        print('# of Queries: {}'.format(len(connection.queries)))
        return response
    '''