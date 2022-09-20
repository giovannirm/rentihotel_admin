from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'registro_adicional'

urlpatterns = [
    path('hotels/<int:pk_h>/room-records/<int:pk_r>/additional-records',RegisterGroupAdditionalByRoom.as_view())
]
