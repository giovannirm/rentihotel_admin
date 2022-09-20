from django.urls import path
#from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'adicional'


additional_create = AdditionalViewSet.as_view({
    #'post' : 'create',
    'get' : 'list'
})
additional_actions = AdditionalViewSet.as_view({
    'get': 'retrieve',
    #'put'   : 'update',
    #'delete': 'destroy'
})

urlpatterns = [
    path('hotels/<int:pk_h>/additionals', additional_create, name='additional_create'),
    #path('hotels/<int:pk_h>/additionals/<int:pk>', additional_actions, name='additional_actions'),
]
