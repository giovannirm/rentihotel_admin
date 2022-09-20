from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'cliente'

customer_hotel_create = HotelCustomersViewSet.as_view({
    'post' : 'create',
    'get' : 'list'
})
customer_hotel_actions = HotelCustomersViewSet.as_view({
    'get': 'retrieve',
    'put'   : 'update',
    #'delete': 'destroy'
})


urlpatterns = [
    path('hotels/<int:pk>/search-customers', CustomerSearchByHotel.as_view()),
    path('hotels/<int:pk_h>/customers', customer_hotel_create, name='customer_create'),
    path('hotels/<int:pk_h>/customers/<int:pk>', customer_hotel_actions, name='customer_actions')
]



