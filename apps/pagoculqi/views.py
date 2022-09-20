import json
import requests
from django.http import JsonResponse
from django.db import connection
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string

from .serializers import *
from .models import PagoCulqi
from reserva.models import Reserva
from registrocliente.models import RegistroCliente
from usuario.models import User

from utils.cursor import dict_detail_reservation , dictfetchall

from settings import CULQI_PRIVATE_KEY , EMAIL_HOST_USER

URL = "https://api.culqi.com/v2/charges"

header = {
    "Content-type" : "application/json",
    "Authorization": "Bearer %s" % CULQI_PRIVATE_KEY
}


def index(request):
    return render(request, 'culqi.html')

class CulqiChargesView(APIView):
    permission_classes = ()  
    def post(self, request, format=None):     
        serializer = ChargeClientSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            reservation = Reserva.objects.get(pk=serializer.validated_data['reservation']) # buscando la reserva
            customer = RegistroCliente.objects.get(pk=serializer.validated_data['customer_registration']) # buscando el cliente
            user_hotel = User.objects.get(hotel__id=reservation.hotel_id,tipo_usuario='ADMIN_HOTEL')
        except Exception as e:
            exc = { 'error c': str(e) }
            return Response(exc, status=status.HTTP_404_NOT_FOUND)
        
        # Api - Culqi
        try:
            response = requests.post(URL,data=json.dumps(serializer.validated_data['charge']), headers=header)
            charge = response.json()
            if response.status_code != 201:
                return Response ({
                    'type_error':charge['type'], 
                    'merchant_message' : charge['merchant_message'] }, 
                    status=response.status_code)
        except Exception as e:
            return Response({'message': str(e)}, status=response.status_code) 
       
        #Tabla Culqi  
        pagoCulqi = PagoCulqi(registro_cliente=customer.id,cargo=charge['id'],reserva=reservation.id)
        pagoCulqi.save()  

        #reservation.estado_reserva = 'RESERVADO'
        #reservation_customer.save() 
        
        try:            
            with connection.cursor() as cursor:
                cursor.callproc('fn_reservation_detail_customer',[reservation.id,])
                data = cursor.fetchall()  
                result= dict_detail_reservation(cursor,data)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
        result['user_hotel'] = user_hotel.first_name    
        mail_host= EmailMessage('Nueva Reserva ', render_to_string('host_mail.html', result), to=[user_hotel.email]) #customer.correo_electronico,
        mail_host.content_subtype = 'html'
        mail_host.send() 

        mail_customer = EmailMessage('Confirmación de Reserva ', render_to_string('customer_mail.html', result),to=[customer.correo_electronico,EMAIL_HOST_USER]) #customer.correo_electronico,
        mail_customer.content_subtype = 'html'
        mail_customer.send()   
        
        return Response({'message':'ok'},status=status.HTTP_200_OK)
    
    
    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        # For debugging purposes only.
        from django.db import connection
        #print(connection.queries)
        #print('# of Queries: {}'.format(len(connection.queries)))
        return response
    