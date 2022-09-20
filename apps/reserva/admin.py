from django.contrib import admin
from .models import Reserva

class Reserva_Admin(admin.ModelAdmin):
    list_display =('id','codigo_reserva','hotel','registro_cliente','estado_reserva','precio_total','fecha_registro')
    ordering = ('id',)
    list_filter = ('hotel',)

admin.site.register(Reserva,Reserva_Admin)
