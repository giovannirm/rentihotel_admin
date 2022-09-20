from django.contrib import admin
from .models import RegistroHabitacion

class RegistroHabitacion_Admin(admin.ModelAdmin):
    list_display = ('id','habitacion','registro','estado_habitacion','precio_total')
    ordering = ('id',)
    list_filter = ('registro__hotel_id',)
    ordering = ('id',)

   

admin.site.register(RegistroHabitacion,RegistroHabitacion_Admin)