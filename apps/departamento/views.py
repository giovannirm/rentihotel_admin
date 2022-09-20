from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Departamento
from .serializers import DepartamentoSerializer,DepartRecomendSerializer
from django.db import connection
from utils.cursor import dictfetchall

## MOD - RESERVAS 
class ListDepartmentRecomend(generics.ListAPIView):
    pagination_class = None
    permission_classes = ()
   
    def list (self,request):
        department = ','.join(["'AREQUIPA'","'AYACUCHO'","'CAJAMARCA'","'CUSCO'","'CHICLAYO'","'ICA'","'LIMA'","'LORETO'","'PUNO'","'TRUJILLO'"])
        query = "SELECT id,nombre, image as imagen  FROM departamento_departamento WHERE UPPER(nombre) IN (%s)" % department
        try:            
            with connection.cursor() as cursor:
                cursor.execute(query)
                data = cursor.fetchall()       
                result = dictfetchall(cursor,data)
                serializer = DepartRecomendSerializer(result,many=True)
                return Response(serializer.data)      
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

## MOD - GESTION
class ListDepartment(generics.ListAPIView):
    pagination_class = None
    permission_classes = ()
    serializer_class = DepartamentoSerializer
    def get_queryset(self):
        queryset =Departamento.objects.filter(pais=self.kwargs["pk"]).order_by('id')
        return queryset
        

