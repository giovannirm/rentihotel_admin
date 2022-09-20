import re
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User

## MOD - RESERVA
class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'first_name', 'last_name','birth_date','password','pais','tipo_usuario']
        extra_kwargs = {'password': {'write_only': True}} 
        
    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("La contraseña es muy corta. Debe contener al menos 6 caracteres.")
        if value.isalpha()  or value.isdigit() :
            raise serializers.ValidationError("La contraseña debe ser alfanumérica.")
        if re.search(' ',value)  is not None:
            raise serializers.ValidationError("La contraseña no debe contener espacios.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(username = validated_data['email'],**validated_data)
        if password is not None:
            instance.set_password(password)        
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

class ResetPasswordSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(required=True,min_length=6,max_length=30)
    new_password2 = serializers.CharField(required=True,min_length=6,max_length=30)
    
    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError("Los dos campos de contraseña no coinciden")
        return data

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True,min_length=6,max_length=30)
    confirmed_password = serializers.CharField(required=True,min_length=6,max_length=30)

    def validate_new_password(self, value):
        validate_password(value)  # devuelve None si las validaciones son correctas
        return value

## MOD - GESTION   

class UserDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','username','first_name', 'last_name','birth_date','pais']