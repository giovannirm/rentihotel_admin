from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'tipo_habitacion'


urlpatterns = [
    path('hotels/<int:pk>/room-types',TypeRoomSelectView.as_view())

]
