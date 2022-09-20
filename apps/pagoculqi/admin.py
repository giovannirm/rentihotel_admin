from django.contrib import admin
from .models import PagoCulqi

class PagoCulqi_Admin(admin.ModelAdmin):
    list_display = ('registro_cliente','reserva','cargo','fecha_registro',)

admin.site.register(PagoCulqi,PagoCulqi_Admin)