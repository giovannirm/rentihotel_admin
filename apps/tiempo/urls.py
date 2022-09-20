from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

app_name = 'tiempo'

#router = DefaultRouter()
#router.register('time', TimeViewSet ,basename='time_administration')

urlpatterns = [
    path('hotels/<int:pk_h>/types-room/<int:pk_tr>/times',TimeSelectView.as_view())
]
#urlpatterns += router.urls