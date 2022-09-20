from rest_framework import serializers
from .models import Hospedante
from hotel.models import Hotel
from registrohabitacion.models import RegistroHabitacion

class HospedanteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Hospedante
        fields = '__all__'


class HostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Hospedante
        exclude = ['usuario_registra', 'fecha_registro','usuario_actualiza', 'fecha_actualiza']
    
    def validate(self, data):
        hotel_id = self.context.get('request').parser_context['kwargs']['pk_h']
        try:
            hotel = Hotel.objects.get(pk=hotel_id)
            return data
        except Hotel.DoesNotExist:
            raise serializers.ValidationError("El hotel no existe")

    def create(self,validated_data):
        user = self.context['request'].user
        host = Hospedante.objects.create(usuario_registra=user.id,**validated_data)
        return host
    
    def update (self,instance,validated_data):
        user = self.context['request'].user 
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.usuario_actualiza = user.id  
        instance.save()
        validated_data['id']= instance.pk
        return validated_data





# detalle en el serializaodr de registro
class HostRegisterRoomSerializers(serializers.ModelSerializer):
    class Meta:
        model = Hospedante
        fields = ['id','nombre','apellido','tipo_documento','numero_documento','genero', 'edad','celular','correo_electronico','nacionalidad','residencia','motivo_viaje'  ]
        #exclude = ['usuario_registra', 'fecha_registro','usuario_actualiza', 'fecha_actualiza']
   
    
    def validate(self, data):
        hotel_id = self.context.get('request').parser_context['kwargs']['pk_h']
        record_room_id = self.context.get('request').parser_context['kwargs']['pk_r']
        try:
            record_room = RegistroHabitacion.objects.get(pk=record_room_id,registro__hotel_id=hotel_id)
        except RegistroHabitacion.DoesNotExist:
            raise serializers.ValidationError("El registro no existe")
        return data
    
    def create(self,validated_data):
        user = self.context['request'].user
        record_room_id = self.context.get('request').parser_context['kwargs']['pk_r']
        hotel_id = self.context.get('request').parser_context['kwargs']['pk_h']

        host = Hospedante.objects.create(usuario_registra=user.id,**validated_data)
        record_room = RegistroHabitacion.objects.get(pk=record_room_id,registro__hotel_id=hotel_id)
        record_room.hospedantes.add(host)
        return host
    
    def update (self,instance,validated_data):
        user = self.context['request'].user 
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.usuario_actualiza = user.id  
        instance.save()
        validated_data['id']= instance.pk
        return validated_data



