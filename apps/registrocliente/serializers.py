from rest_framework import serializers
from .models import RegistroCliente

class RegisterClientSerializers(serializers.ModelSerializer):
    class Meta:
        model = RegistroCliente
        fields = '__all__'

class RegisterCustomerSerializers(serializers.ModelSerializer):
    class Meta:
        model = RegistroCliente
        exclude = ['tipo_cliente','fecha_registro']

class RecordCustomerSerializers(serializers.ModelSerializer):
    class Meta:
        model = RegistroCliente
        fields = ['id','numero_documento']

