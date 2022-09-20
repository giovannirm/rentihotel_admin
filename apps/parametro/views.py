from django.http import JsonResponse

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from utils.permission import  IsAdmin,IsOwner,IsOwnerOrAdmin
from .models import Parametro
from .serializers import *

class GroupListParameters(generics.ListAPIView):
    pagination_class = None
    permission_classes = ()
    def list (self,request):
        group = request.query_params.get('group')
        if group :
            queryset = Parametro.objects.all().filter(grupo__istartswith=group,estado='ACT').order_by('id')
        else:
            queryset = Parametro.objects.all()

        serializers =  GroupListParamsSerializers(queryset,many=True)
        return Response(serializers.data)
        