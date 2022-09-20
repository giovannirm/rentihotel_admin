from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'registro_cliente'
#router = DefaultRouter()
#router.register('register-customers',RegistroClientViewSet,basename='register-customer_administration')
urlpatterns = [
    path('register-customer',RegisterCostumer.as_view()),
    
]
#urlpatterns +=router.urls