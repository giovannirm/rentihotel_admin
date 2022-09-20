from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'registro'

record_create = RecordViewSet.as_view({
    'post':'create',
    'get':'list'
})

record_action = RecordViewSet.as_view({
    'get':'retrieve',
    #'put': 'update',
    #'delete': 'destroy'
})

urlpatterns = [
    path('hotels/<int:pk_h>/records' , record_create ),
    path('hotels/<int:pk_h>/reservation-records' , RegisterReservationRecord.as_view()),
    path('hotels/<int:pk_h>/records/<int:pk>' , record_action),
    path('hotels/<int:pk_h>/room-booking',RoomBookingView.as_view()),
    path('hotels/<int:pk_h>/room-booking/v2',RoomBookingViewV2.as_view()),
    
    #path('hotels/<int:pk_h>/h-records',RoomBookingView.as_view())
]

##SELECT * from fn_room_booking_multiple_json(1,'2020-04-04','2020-06-28',ARRAY [1, 3])