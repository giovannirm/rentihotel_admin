from django.contrib import admin
from .models import Cliente

class Cliente_Admin(admin.ModelAdmin):
    list_display = ('id', 'nombre','numero_documento')
    readonly_fields =('fecha_registro','fecha_actualiza',)
    ordering = ('id',)
    list_filter = ('registro__hotel',)

    fieldsets = (
        (None, {'fields': ('nombre','apellido','tipo_documento','numero_documento','genero','edad')}),
        (('Contacto'), {'fields': ('celular', 'correo_electronico')}),
        (('Información Adicional'), {'fields': ('nacionalidad', 'residencia','motivo_viaje')}),
        (('Create'), {'fields': ('usuario_registra', 'fecha_registro')}),
        (('Update'), {'fields': ('usuario_actualiza', 'fecha_actualiza')}),        
    )



admin.site.register(Cliente,Cliente_Admin)
