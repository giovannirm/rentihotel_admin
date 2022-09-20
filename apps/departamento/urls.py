from django.urls import path 
from .views import *

app_name = 'departamento'

urlpatterns = [
    path('paises/<int:pk>/departmentos',ListDepartment.as_view()),
    path('recommended-list',ListDepartmentRecomend.as_view()),
]