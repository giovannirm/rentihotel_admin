from rest_framework import viewsets,generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .models import RegistroCliente
from .serializers  import RegisterClientSerializers

## MOD - RESERVAS 
class RegisterCostumer(generics.CreateAPIView):
    permission_classes = ()
    serializer_class = RegisterClientSerializers



## MOD - GESTION
class RegistroClientViewSet(viewsets.ModelViewSet):
    queryset = RegistroCliente.objects.all()
    serializer_class = RegisterClientSerializers
    permission_classes = ()


