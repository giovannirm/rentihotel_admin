from django.contrib import admin
from .models import Parametro
class Parametro_Admin(admin.ModelAdmin):
    list_display = ('id', 'codigo','nombre','valor','estado')
    readonly_fields =('fecha_registro','fecha_actualiza',)
    ordering = ('id',)
    list_filter = ('grupo',)
    fieldsets = (
        (None, {'fields': ('grupo','codigo', 'nombre','valor','estado')}),
        (('Create'), {'fields': ('usuario_registra', 'fecha_registro')}),
        (('Update'), {'fields': ('usuario_actualiza', 'fecha_actualiza')}),        
    )
    
admin.site.register(Parametro,Parametro_Admin)