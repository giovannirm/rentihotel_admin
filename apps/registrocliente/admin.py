from django.contrib import admin
from .models import RegistroCliente

class RegistroCliente_Admin(admin.ModelAdmin):
    list_display =('id','nombre','numero_documento','tipo_cliente','fecha_registro')
    list_filter = ('reserva__hotel_id',)
    ordering = ('id',)


admin.site.register(RegistroCliente,RegistroCliente_Admin)
