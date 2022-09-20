from django.contrib import admin
from .models import Habitacion

class Habitacion_Admin(admin.ModelAdmin):
    list_display =('id', 'numero_habitacion','tipo_habitacion' , 'estado_habitacion' ,'hotel')
    ordering = ('id',)
    list_filter = ('hotel',)

admin.site.register(Habitacion, Habitacion_Admin)