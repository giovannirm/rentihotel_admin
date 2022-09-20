from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'habitacion'

urlpatterns = [
    path('hotels/<int:pk>/rooms',ListRoomsByHotelView.as_view())
]
