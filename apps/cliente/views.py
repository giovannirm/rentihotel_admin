from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404 
from django.http import JsonResponse
from django.db import connection
from utils.cursor import dictfetchall , dictfetchone
from utils.permission import IsUserManagment

from hotel.models import Hotel
from .models import Cliente
from .serializers import * 

class CustomerSearchByHotel(APIView):
    permission_classes = ([ IsUserManagment, ])  

    def get_queryset(self,pk):
        try:
            obj  = Hotel.objects.get(pk=pk)
            queryset = Cliente.objects.filter(registro__hotel=pk).order_by('id').distinct()
            return queryset
        except Hotel.DoesNotExist:
            raise Http404("Hotel does not exist")

    def post(self ,request,pk=None,*arg, **kwargs):
        numero_documento = request.data.get('numero_documento')
        tipo_documento = request.data.get('tipo_documento')
        if numero_documento and tipo_documento:  
            customers = self.get_queryset(pk).filter(numero_documento=numero_documento,tipo_documento=tipo_documento)
            serializers = HotelCustomersSerializers(customers ,many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)            
        return Response({ 'message': 'Request could not be performed with received data.'}, status=status.HTTP_400_BAD_REQUEST) 
    
    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        # For debugging purposes only.
        from django.db import connection
        #print(connection.queries)
        #print('# of Queries: {}'.format(len(connection.queries)))
        return response
    
class HotelCustomersViewSet(viewsets.ModelViewSet):
    permission_classes = ([ IsUserManagment, ])    
    serializer_class = HotelCustomersSerializers
    queryset = Cliente.objects.all()
 
    def get_serializer_context(self):
        return { "request": self.request }
    
    def get_queryset(self):
        try:
            obj  = Hotel.objects.get(pk=self.kwargs['pk_h'])
            queryset = self.queryset.filter(registro__hotel=self.kwargs['pk_h']).order_by('id').distinct()
            return queryset
        except Hotel.DoesNotExist:
            raise Http404("Hotel does not exist")

    def get_object(self):
        try:
            return self.get_queryset().get(pk=self.kwargs['pk'])
        except Cliente.DoesNotExist:
            raise Http404

    def create(self,request,pk_h):
        serializer = HotelCustomersSerializers(data=request.data,context={ "request": self.request }) 
        serializer.is_valid(raise_exception=True)
        if request.data.get('id'):
            try:
                customer = self.get_queryset().get(pk=request.data.get('id'))       
                update_customer  = HotelCustomersSerializers(customer, data=request.data ,context={ "request": self.request })
                update_customer.is_valid(raise_exception=True)
                update_customer.save()
                return Response(update_customer.data,status=status.HTTP_201_CREATED)
        
            except Cliente.DoesNotExist:
                return Response({ 'message':'Customer not found to update.'}, status=status.HTTP_404_NOT_FOUND) 

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





##ALL CLIENTS
class CustomersViewSet(viewsets.ModelViewSet):
    permission_classes = ([ IsUserManagment, ])    
    serializer_class = CustomerSerializers
    queryset = Cliente.objects.all()
 
    def get_serializer_context(self):
        return { "request": self.request }

'''
path('customers', customer_create, name='customer_create'),
path('customers/<int:pk>', customer_actions, name='customer_actions')
class CustomerViewSetV1(viewsets.ModelViewSet):
    pagination_class = None
    queryset = Cliente.objects.all()
    serializer_class = CustomerSerializers
'''
    