from django.contrib import admin
from .models import RegistroAdicional

class RegistroAdicional_Admin(admin.ModelAdmin):
     list_display = ('id','registro_habitacion','adicional','tipo_adicional','cantidad','precio_total')
     list_filter = ('registro_habitacion__registro__hotel_id',)
     ordering = ('id',)


admin.site.register(RegistroAdicional,RegistroAdicional_Admin)


