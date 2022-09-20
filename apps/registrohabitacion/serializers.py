from rest_framework import serializers
from .models import RegistroHabitacion

from registroadicional.models import RegistroAdicional
from hospedante.models import Hospedante

from hospedante.serializers import HostRegisterRoomSerializers
from registroadicional.serializers import RegisterAdditionalSerializers

from registro.models import Registro
from habitacion.models import Habitacion
from hotel.models import Hotel

# PARA --> solo registro habitacion sin relaciones 
class RoomRecordSerializers(serializers.ModelSerializer):
    class Meta:
        model = RegistroHabitacion
        #fields = ['id','habitacion','estado_habitacion','fecha_ingreso','fecha_salida','codigo','tiempo','cantidad_adulto','cantidad_nino','precio','precio_total']
        exclude = ['usuario_registra', 'fecha_registro','usuario_actualiza', 'fecha_actualiza','registro','hospedantes']
    '''
    def validate(self, data):
        hotel = self.context.get('request').parser_context['kwargs']['pk_h']
        try:
            hotel = Hotel.objects.get(pk=hotel)
            habitacion = Habitacion.objects.get(pk=data['habitacion'],hotel_id=hotel)  
            return data
        except Hotel.DoesNotExist:
            raise serializers.ValidationError("El hotel no existe")                  
        except Habitacion.DoesNotExist:
            raise serializers.ValidationError("La Habitacion no existe")

    def create(self,validated_data):
        user = self.context['request'].user
        record_room = RegistroHabitacion.objects.create(usuario_registra=user.id,**validated_data)
        return record_room
    
    def update (self,instance,validated_data):
        user = self.context['request'].user 
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.usuario_actualiza = user.id  
        instance.save()
        validated_data['id']= instance.pk
        return validated_data
    '''



# Detalle mas relaciones de r.a.
class RoomRegisterDetailSerializers(serializers.ModelSerializer):
    hospedantes = HostRegisterRoomSerializers(many=True)
    registros_adicional = RegisterAdditionalSerializers(many=True)
    class Meta:
        model = RegistroHabitacion
        exclude = ['usuario_registra', 'fecha_registro','usuario_actualiza', 'fecha_actualiza','hospedantes']
        
   
class CompleteRoomRecordSerializers(serializers.ModelSerializer):
    class Meta:
        model = RegistroHabitacion
        #fields = '__all__'
        exclude = ['registro','usuario_registra', 'fecha_registro','usuario_actualiza', 'fecha_actualiza']

    def validate(self, data):
        record_id = self.context.get('request').parser_context['kwargs']['pk_r']
        try:
            record = record.objects.get(pk=record_id)
            return data
        except Registro.DoesNotExist:
            raise serializers.ValidationError("Record does not exist")

    def create(self,validated_data):
        user = self.context['request'].user
        registro = self.context.get('request').parser_context['kwargs']['pk_r']
        record_room = RegistroHabitacion.objects.create(usuario_registra=user.id,registro_id=registro,**validated_data)
        return record_room
    
    def update (self,instance,validated_data):
        user = self.context['request'].user 
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.usuario_actualiza = user.id  
        instance.save()
        validated_data['id']= instance.pk
        return validated_data










