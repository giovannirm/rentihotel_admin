from django.contrib import admin
from .models import Pais

class Pais_Admin(admin.ModelAdmin):
    ordering = ('id',)
    list_display =('codigo', 'nombre')

admin.site.register(Pais, Pais_Admin)