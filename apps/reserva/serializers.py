from rest_framework import serializers

from .models import Reserva
from reservadetalle.serializers import RegisterReservationDetailSerializers , ReservationDetailSerializers
from reservadetalle.models import ReservaDetalle
from registrocliente.serializers import RegisterCustomerSerializers

from django.db.models import Avg, Count, Min, Sum

## MOD RESERVAS
class ReservationsCustomerSerializers(serializers.ModelSerializer):
    reserva_detalle = RegisterReservationDetailSerializers(many=True)
    class Meta:
        model = Reserva
        fields = '__all__'
 
    def create(self,validated_data):
        reservation = Reserva(            
            hotel_id = validated_data.get("hotel"),
            registro_cliente = validated_data.get("registro_cliente"),
            fecha_ingreso = validated_data.get("fecha_ingreso"),
            fecha_salida = validated_data.get("fecha_salida"),
            hora_llegada = validated_data.get("hora_llegada"),
            estado_reserva = validated_data.get("estado_reserva"),
            cantidad_adulto = validated_data.get("cantidad_adulto"),
            cantidad_nino = validated_data.get("cantidad_nino"),
            subtotal = validated_data.get("subtotal"),
            igv = validated_data.get("igv"),
            precio_total = validated_data.get("precio_total"),
            tipo_pago = validated_data.get("tipo_pago"),
            adelanto = validated_data.get("adelanto")           
        )
        reservation.save()
        reservations_detail = validated_data.get('reserva_detalle')
        serializer = RegisterReservationDetailSerializers(data=reservations_detail,many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(reserva_id=reservation.id)
        validated_data['reserva_detalle'] = serializer.data

        '''
        for i in range(len(reservations_detail)):
            serializers = RegisterReservationDetailSerializers(data=reservations_detail[i])
            serializers.is_valid(raise_exception=True)
            serializers.save(reserva=reservation)
            reservations_detail[i] = serializers.data
        '''
        validated_data['id'] = reservation.id
        return validated_data

## MOD GESTION
class ReservationSerializers(serializers.ModelSerializer):
    reserva_detalle = serializers.SerializerMethodField()
    registro_cliente = serializers.SlugRelatedField(
        read_only=True,
        slug_field='numero_documento'
    )
       
    class Meta:
        model = Reserva
        fields = ['id','codigo_reserva','fecha_ingreso','fecha_salida','reserva_detalle','estado_reserva','registro_cliente']
    
    def get_reserva_detalle(self, instance):
        #cantidad2 = ReservaDetalle.objects.filter(reserva_id=instance.id).aggregate(Sum('cantidad'))    
        cantidad = instance.reserva_detalle.all().aggregate(Sum('cantidad'))['cantidad__sum']    
        return cantidad



class ReservationDetailSerializers(serializers.ModelSerializer):
    registro_cliente = RegisterCustomerSerializers()
    reserva_detalle = ReservationDetailSerializers(many=True)
    class Meta:
        model = Reserva
        #fields = '__all__'
        exclude = ['hotel']
        