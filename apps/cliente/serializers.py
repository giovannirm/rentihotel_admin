from rest_framework import serializers
from .models import Cliente
from hotel.models import Hotel

class ClienteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
    

class HotelCustomersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        exclude = ['usuario_registra', 'fecha_registro','usuario_actualiza', 'fecha_actualiza']
    
    def validate(self, data):
        hotel_id = self.context.get('request').parser_context['kwargs']['pk_h']
        try:
            hotel = Hotel.objects.get(pk=hotel_id)
        except Hotel.DoesNotExist:
            raise serializers.ValidationError("El hotel no existe")
        return data
    
    def create(self,validated_data):
        user = self.context['request'].user
        customer = Cliente.objects.create(usuario_registra=user.id,**validated_data)
        return customer
        

    def update (self,instance,validated_data):
        user = self.context['request'].user 
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.usuario_actualiza = user.id  
        instance.save()
        validated_data['id']= instance.pk
        return validated_data

class CustomerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        exclude = ['usuario_registra', 'fecha_registro','usuario_actualiza', 'fecha_actualiza']
    
    def create(self,validated_data):
        user = self.context['request'].user
        customer = Cliente.objects.create(usuario_registra=user.id,**validated_data)
        return customer        

    def update (self,instance,validated_data):
        user = self.context['request'].user 
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.usuario_actualiza = user.id  
        instance.save()
        validated_data['id']= instance.pk
        return validated_data
