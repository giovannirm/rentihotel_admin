from rest_framework import serializers
from .models import Tiempo

## MOD RESERVAS
class TimeCalcPriceSerializers(serializers.ModelSerializer):
    class Meta :
        model = Tiempo
        fields = ['id','codigo','valor','precio']


## MOD GESTION


## MOD GESTION
class TimeSelectSerializers(serializers.ModelSerializer):
    class Meta :
        model = Tiempo
        fields = ['id','codigo','precio','promocion']



class TiempoSerializers(serializers.ModelSerializer):
    class Meta :
        model = Tiempo
        fields = '__all__'
