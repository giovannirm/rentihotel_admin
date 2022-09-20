from django.contrib import admin
from .models import Departamento

class Departamento_Admin(admin.ModelAdmin):
    list_display =('codigo', 'nombre')
    list_filter = ('pais',)
    ordering = ('id',)

admin.site.register(Departamento, Departamento_Admin)
