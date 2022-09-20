from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'reserva'


reservation_create = ReservationViewSet.as_view({
    'get' :'list',
    #'post' : 'create'
})

reservation_actions = ReservationViewSet.as_view({
    'get': 'retrieve',
    'put'   : 'update',
    #'delete': 'destroy'
})
urlpatterns = [
    path('reservations',ReservationCustomerView.as_view()),
    #path('lista',ReservationCustomerLIST.as_view()),
    
    path('hotels/<int:pk_h>/reservations', reservation_create),
    path('hotels/<int:pk_h>/reservations/<int:pk>', reservation_actions)
    
]
