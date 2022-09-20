from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'hospedante'

host_room_create = HostRegisterRoomViewSet.as_view({
    'get' :'list',
    'post' : 'create'
})
host_room_actions = HostRegisterRoomViewSet.as_view({
    'get': 'retrieve',
    'put'   : 'update',
    #'delete': 'destroy'
})

host_create = HostByHotelViewSet.as_view({
    'get' :'list',
    #'post' : 'create'
})
host_actions = HostByHotelViewSet.as_view({
    'get': 'retrieve',
    #'put'   : 'update',
    #'delete': 'destroy'
})

urlpatterns = [
    path('hotels/<int:pk>/search-hosts', HostSearchByHotel.as_view()),
    path('hotels/<int:pk_h>/room-records/<int:pk_r>/hosts', host_room_create),
    path('hotels/<int:pk_h>/room-records/<int:pk_r>/hosts/<int:pk>', host_room_actions),

    path('hotels/<int:pk_h>/hosts', host_create, name='host_create'),
    path('hotels/<int:pk_h>/hosts/<int:pk>', host_actions, name='host_actions'),

]





