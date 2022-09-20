from rest_framework import serializers
from .models import ReservaDetalle

## MOD - RESERVA

class RegisterReservationDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = ReservaDetalle
        fields = ['id','tipo_habitacion','precio_total','tiempo','cantidad']
        


## MOD - GESTION 
class ReservationDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = ReservaDetalle
        exclude = ['reserva','fecha_registro']


