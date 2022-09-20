from django.contrib import admin
from .models import ReservaDetalle

class ReservaDetalle_Admin(admin.ModelAdmin):
    list_display =('id','reserva','tipo_habitacion','precio_total','fecha_registro',)
    ordering = ('id',)

admin.site.register(ReservaDetalle,ReservaDetalle_Admin)