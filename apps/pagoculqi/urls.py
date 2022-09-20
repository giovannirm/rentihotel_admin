from django.urls import path
from .views import *

app_name = 'pagosCulqi'

urlpatterns = [
    path('index', index, name='index'),
    path('charges', CulqiChargesView.as_view() , name='charges')
]
