from django.contrib import admin
from .models import TipoHabitacion

class TipoHabitacion_Admin(admin.ModelAdmin):
    ordering = ('id',)
    list_display =('id','nombre', 'descripcion','hotel')
    list_filter = ('hotel',)
    
admin.site.register(TipoHabitacion, TipoHabitacion_Admin)

