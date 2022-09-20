from rest_framework import serializers
from .models import PagoCulqi

class PagoCulqiSerializers(serializers.ModelSerializer):
      model = PagoCulqi
      fields = '__all__'


class ChargeSerializers(serializers.Serializer):
      amount = serializers.IntegerField()  
      currency_code =  serializers.CharField()
      description = serializers.CharField(required=False) 
      email = serializers.EmailField()           
      source_id = serializers.CharField()
      installments = serializers.IntegerField(required=False)

class ChargeClientSerializers(serializers.Serializer):
      charge = ChargeSerializers()
      customer_registration = serializers.IntegerField()
      reservation = serializers.IntegerField()
     