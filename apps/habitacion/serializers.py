from rest_framework import serializers
from .models import Habitacion

class HabitacionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Habitacion
        fields = '__all__'


class ListRoomsByHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habitacion
        fields = ['id','numero_habitacion','numero_piso','tipo_habitacion','estado_habitacion']
