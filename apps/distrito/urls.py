from django.urls import path 
from .views import *
from .ajax import get_provincias

app_name = 'distrito'

urlpatterns = [    
  path('distrito/<int:pk>',ListaDistrito.as_view()),
]