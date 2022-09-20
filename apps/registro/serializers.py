from rest_framework import serializers
from django.db.models import Prefetch
from .models import Registro
from hotel.models import Hotel
from  registrohabitacion.serializers import RoomRecordSerializers  ,RoomRegisterDetailSerializers
from registrohabitacion.models import RegistroHabitacion
from registrocliente.serializers import RecordCustomerSerializers



# --> registro + registro_habitacion  
class RecordSerializers(serializers.ModelSerializer):
    registros_habitacion = RoomRecordSerializers(many=True)
    class Meta:
        model = Registro
        exclude = ['usuario_registra', 'fecha_registro','usuario_actualiza', 'fecha_actualiza','hotel']
  
    def create(self,validated_data):
        user = self.context.get('request').user
        hotel = self.context.get('request').parser_context['kwargs']['pk_h']
        record = Registro(
            cliente = validated_data.get('cliente'),
            hotel_id=hotel,
            reserva = validated_data.get('reserva'),
            estado_registro = validated_data.get('estado_registro'),
            tipo_pago = validated_data.get('tipo_pago'),
            adelanto = validated_data.get('adelanto'),
            precio_total = validated_data.get('precio_total'),
            usuario_registra=user.id
            )
        record.save()

        records_room =  validated_data.get('registros_habitacion')   

        for i in range(0,len(records_room)):
            serializer = RoomRecordSerializers( data=records_room[i], context = { 'request': self.context.get('request') } )
            serializer.is_valid(raise_exception=True)
            serializer.save(registro=record) 
            records_room[i] = serializer.data 

        validated_data['registros_habitacion'] = records_room 
        validated_data['id'] = record.id   

        return validated_data
    
    @staticmethod
    def record_prefetch(queryset):
        queryset = queryset.prefetch_related('registros_habitacion')
        return queryset

class RecordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registro
        fields = ['id','estado_registro','fecha_registro','reserva']

class ReservationRecordSerializer(serializers.Serializer):
    registro_cliente = RecordCustomerSerializers(required=True)
    registro = RecordSerializers(required=True)









class OnlyRecordSerializers(serializers.ModelSerializer):
    class Meta:
        model = Registro
        #fields = '__all__'
        exclude = ['usuario_registra', 'fecha_registro','usuario_actualiza', 'fecha_actualiza','hotel']

    def validate(self, data):
        hotel = self.context.get('request').parser_context['kwargs']['pk_h']
        try:
            hotel = Hotel.objects.get(pk=hotel)
            return data
        except Hotel.DoesNotExist:
            raise serializers.ValidationError("El hotel no existe")
    
    
    def create(self,validated_data):
        user = self.context['request'].user
        hotel = self.context.get('request').parser_context['kwargs']['pk_h']
        record = Registro.objects.create(usuario_registra=user.id,hotel_id=hotel,**validated_data)
        return record
    
    def update (self,instance,validated_data):
        user = self.context['request'].user 
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.usuario_actualiza = user.id  
        instance.save()
        validated_data['id']= instance.pk
        return validated_data

# detalle extendido
class RecordDetailSerializers(serializers.ModelSerializer):
    registros_habitacion = RoomRegisterDetailSerializers(many=True)
    class Meta:
        model = Registro
        #fields = [ 'id','reserva','cliente','fecha_ingreso','fecha_salida','estado_registro','cantidad_huesped','precio','tipo_pago','adelanto','precio_total','registros_habitacion']
        exclude = ['usuario_registra','fecha_registro','usuario_actualiza', 'fecha_actualiza','hotel']

    @staticmethod
    def record_prefetch(queryset):
        groups_type = Prefetch('registros_habitacion',RegistroHabitacion.objects.prefetch_related('registros_adicional','hospedantes'))
        queryset = queryset.prefetch_related(groups_type)
        return queryset














