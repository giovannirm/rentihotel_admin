from django.contrib import admin
from .models import Tiempo

class Tiempo_Admin(admin.ModelAdmin):
    ordering = ('id',)
    list_display =('id','codigo', 'precio','tipo_habitacion')
    list_filter = ('tipo_habitacion__hotel',)

admin.site.register(Tiempo, Tiempo_Admin)