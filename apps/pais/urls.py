from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ListaPaisesView


urlpatterns = [    
  path('paises', ListaPaisesView.as_view(),name='Lista Paises')
]

