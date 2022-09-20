from django.urls import path 
from .views import ListProvincia

urlpatterns = [    
  path('api/filter-provincia/<int:pk>',ListProvincia.as_view()),
]