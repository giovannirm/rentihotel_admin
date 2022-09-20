from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

app_name = 'hotel'

hotel_list = HotelsViewSet.as_view({
    'get': 'list',   
})

hotel_detail = HotelsViewSet.as_view({
    'get': 'retrieve',    
})


urlpatterns = [   
    path('hotels/search',SearchHotelsByPlace.as_view()),
    path('hotels', hotel_list),
    path('hotels/<int:pk>', hotel_detail),    
    path('users/<int:pk>/hotels',UserHotelsView.as_view()),
]






'''
hotel_list = HotelViewSet.as_view({
    'get': 'list',   
    'post': 'create' 
})
hotel_create = HotelViewSet.as_view({
    'post': 'create'
})
hotel_detail = HotelViewSet.as_view({
    'get': 'retrieve',    
    'put': 'update',
    'delete': 'destroy'
})
urlpatterns = format_suffix_patterns([
    #path('api/ppp',HotelCreateAPIView.as_view()),
    path('api/hotels', hotel_list, name='hotels-list'),
    path('api/hotel', hotel_create, name='hotel-create'),
    path('api/hotel/<int:pk>', hotel_detail, name='hotel-detail'),
])

'''