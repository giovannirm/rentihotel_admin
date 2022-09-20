from rest_framework import serializers
from .models import Servicio


## MOD RESERVAS
class DetailServiceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        exclude = ['tipo_habitacion']



## MOD GESTION 
class ServicioSerializers(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'