from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'parametro'

urlpatterns = [
    path('parameters',GroupListParameters.as_view()),
]
