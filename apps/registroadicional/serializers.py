from rest_framework import serializers
from .models import RegistroAdicional
from registrohabitacion.models import RegistroHabitacion
from adicional.models import Adicional

class RegisterAdditionalSerializers(serializers.ModelSerializer):
    class Meta:
        model = RegistroAdicional
        fields = ['id','adicional','cantidad','tipo_adicional','precio_total']

class Serializers(serializers.ModelSerializer):
    class Meta:
        model = RegistroAdicional
        fields = '__all__'


''' 
    def validate(self, data):
        hotel_id = self.context.get('request').parser_context['kwargs']['pk_h']
        record_room_id = self.context.get('request').parser_context['kwargs']['pk_r']
        try:
            record_room = RegistroHabitacion.objects.get(pk=record_room_id,registro__hotel_id=hotel_id)
            additional = Adicional.objects.get(pk=data['adicional'],hotel_id=hotel_id)            
        except RegistroHabitacion.DoesNotExist:
            raise serializers.ValidationError("El registro no existe")
        except Adicional.DoesNotExist:
            raise serializers.ValidationError("El Adicional no existe")
        
        #stock_aditional = additional.cantidad
        #if data['cantidad'] > stock_aditional:
        #    raise serializers.ValidationError("stock insuficiente de Adicional")
        return data
    
    def validate_adicional(self, value):
        hotel_id = self.context.get('request').parser_context['kwargs']['pk_h']
        try:
            additional = Adicional.objects.get(pk=value,hotel_id=hotel_id)            
        except Adicional.DoesNotExist:
            raise serializers.ValidationError("El Adicional no existe")
        return value

    def validate_adicional(self, value):
        hotel_id = self.context.get('request').parser_context['kwargs']['pk_h']
        try:
            additional = Adicional.objects.get(pk=value,hotel_id=hotel_id)            
        except Adicional.DoesNotExist:
            raise serializers.ValidationError("El Adicional no existe")
        return value  
'''
