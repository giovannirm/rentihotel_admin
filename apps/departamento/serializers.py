from rest_framework import serializers
from .models import Departamento

class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = ['id','nombre']


class DepartRecomendSerializer(serializers.ModelSerializer):
    imagen = serializers.CharField()
    class Meta:
        model = Departamento
        fields = ['id','nombre','imagen']