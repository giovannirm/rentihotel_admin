from rest_framework import serializers
from .models import Adicional
from hotel.models import Hotel

class AdditionalSerializers(serializers.ModelSerializer):
    class Meta:
        model = Adicional
        fields = '__all__'
    
    def validate(self, data):
        hotel_id = self.context.get('request').parser_context['kwargs']['pk_h']
        try:
            hotel = Hotel.objects.get(pk=hotel_id)            
        except Hotel.DoesNotExist:
            raise serializers.ValidationError("El hotel no existe")
        return data

    def create(self,validated_data):
        hotel_id = self.context.get('request').parser_context['kwargs']['pk_h']
        additional = Adicional.objects.create(hotel_id=hotel_id,**validated_data)
        return additional


class AdditionalSearchSerializers(serializers.ModelSerializer):
    class Meta:
        model = Adicional
        fields = ['id','nombre','precio','cantidad']
