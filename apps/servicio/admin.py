from django.contrib import admin
from .models import Servicio

class Servicio_Admin(admin.ModelAdmin):
    ordering = ('id',)
    list_display =('id','nombre','tipo_habitacion')
  
admin.site.register(Servicio, Servicio_Admin)
