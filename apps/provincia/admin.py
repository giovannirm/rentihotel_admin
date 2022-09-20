from django.contrib import admin
from .models import Provincia

class Provincia_Admin(admin.ModelAdmin):
    ordering = ('id',)
    list_display =('codigo', 'nombre')
    list_filter = ('departamento',)
   

admin.site.register(Provincia, Provincia_Admin)