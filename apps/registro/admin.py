from django.contrib import admin
from .models import Registro

class Registro_Admin(admin.ModelAdmin):
    list_display =('id','hotel','cliente','reserva','estado_registro','precio_total')
    list_filter = ('hotel',)
    ordering = ('id',)

admin.site.register(Registro,Registro_Admin)

