from rest_framework import serializers
from django.db.models import Prefetch
from django.db.models import Max

from .models import TipoHabitacion

from servicio.serializers import DetailServiceSerializers
from tiempo.serializers import TimeCalcPriceSerializers
from tiempo.models import Tiempo

## MOD RESERVAS
class TypeOfRoomDetailSerializer(serializers.ModelSerializer):
    servicio = DetailServiceSerializers(many=True)
    tiempo = TimeCalcPriceSerializers(many=True)

    class Meta:        
        model = TipoHabitacion
        exclude = ['hotel']
        #fields = '__all__'
    
    @staticmethod
    def room_type_prefetch(queryset):
        queryset = queryset.prefetch_related('servicio')
        queryset = queryset.prefetch_related(Prefetch('tiempo',queryset=Tiempo.objects.filter(codigo='24H')))
        return queryset


## MOD GESTION 
class TypeRoomSelectSerializer(serializers.ModelSerializer):
    class Meta:        
        model = TipoHabitacion
        fields = ['id','nombre','capacidad_persona']






### --------------------------
class TipoHabitacionSerializer(serializers.ModelSerializer):
    class Meta:        
        model = TipoHabitacion
        fields = '__all__'

class TipoHabitacionDetalleSerializer(serializers.ModelSerializer):
    servicio = serializers.SerializerMethodField()
    tiempo = serializers.SerializerMethodField()
     
    class Meta:
        model = TipoHabitacion
        exclude = ['hotel']
    
    def get_servicio(self, instance):
        services = instance.servicio.all().order_by('id')        
        return DetailServiceSerializers(services, many=True).data
    
    def get_tiempo(self,instance):
        times = instance.tiempo.get(codigo='24H')       
        return TimeCalcPriceSerializers(times).data



