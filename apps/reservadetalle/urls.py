from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'ReservaDetalle'

router = DefaultRouter()
router.register('ReservaDetalle', ReservaDetalleViewSet ,basename='_administration')

urlpatterns = [
    
]
urlpatterns += router.urls