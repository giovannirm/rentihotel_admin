from rest_framework import serializers
from .models import Parametro

class ParametroSerializers(serializers.ModelSerializer):
    class Meta:
        model = Parametro
        fields = ['id','codigo','nombre','descripcion','valor','estado']
        #fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        parametro = Parametro.objects.create(usuario_registra=user.id,**validated_data)
        return parametro
    
    def update(self, instance, validated_data):
        user = self.context['request'].user
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.usuario_actualiza = user.id
        instance.save()
        return instance
            


class GroupListParamsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Parametro
        fields = ['id','nombre']
        