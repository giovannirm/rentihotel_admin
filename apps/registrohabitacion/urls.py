from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'RegistroHabitacion'

record_room_create = RecordRoomViewSet.as_view({
    'get':'list',
    'post':'create'
})
record_room_action = RecordRoomViewSet.as_view({
    'get':'retrieve',
    #'put': 'update',
    #'delete': 'destroy'
})


urlpatterns = [
    #path('records/<int:pk_r>/records-room' , record_room_create ),
    #path('records/<int:pk_r>/records-room/<int:pk>' , record_room_action)
]

#urlpatterns += router.urls