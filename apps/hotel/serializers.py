from rest_framework import serializers
from django.db.models import Prefetch

from .models import Hotel

from tipohabitacion.serializers import TypeOfRoomDetailSerializer
from tipohabitacion.models import TipoHabitacion
from tiempo.models import Tiempo

## MOD -Reservas 
class HotelSearchListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(max_length=100 )
    direccion = serializers.CharField(max_length=120 )
    image1 = serializers.CharField()
    image2 = serializers.CharField()
    image3 = serializers.CharField()
    clasificacion = serializers.IntegerField()
    latitud = serializers.CharField()
    longitud = serializers.CharField()
    precio = serializers.DecimalField(decimal_places=2, max_digits=10)

class HotelDetailSerializer(serializers.ModelSerializer):
    pais =serializers.SlugRelatedField( read_only=True,slug_field='nombre' )
    departamento = serializers.SlugRelatedField( read_only=True,slug_field='nombre' )
    provincia = serializers.SlugRelatedField( read_only=True,slug_field='nombre' )
    distrito = serializers.SlugRelatedField( read_only=True,slug_field='nombre' )
    tipo_habitacion = TypeOfRoomDetailSerializer(many=True, read_only=True)    

    class Meta:
        model = Hotel        
        #fields = '__all__'
        exclude = ['usuarios']
        extra_fields = ['tipo_habitacion']

    @staticmethod
    def hotel_prefetch(queryset):
        queryset = queryset.select_related('pais','departamento','provincia','distrito')
        groups_type = Prefetch('tipo_habitacion', queryset=TipoHabitacion.objects.prefetch_related('servicio',Prefetch('tiempo',queryset=Tiempo.objects.filter(codigo='24H'))))
        queryset = queryset.prefetch_related(groups_type)
        return queryset

class HotelListSerializer(serializers.ModelSerializer):
    departamento = serializers.SlugRelatedField( read_only=True,slug_field='nombre' )
    provincia = serializers.SlugRelatedField( read_only=True,slug_field='nombre' )
    distrito = serializers.SlugRelatedField( read_only=True,slug_field='nombre' )
    
    class Meta:
        model = Hotel
        exclude = ['ruc','total_habitacion','telefono','celular','correo_electronico','webpage','fanpage','instagram','pais']

    @staticmethod
    def hotel_prefetch(queryset):
        queryset = queryset.select_related('pais','departamento','provincia','distrito')
        return queryset
      

# MOD - Gestion
class HotelGestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel        
        fields = ['id','nombre','logo']

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'  






#---------------

#Falta Agregar precio
