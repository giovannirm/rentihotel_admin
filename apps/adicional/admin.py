from django.contrib import admin
from .models import Adicional

class Adicional_Admin(admin.ModelAdmin):
    list_display = ('id','nombre','precio','cantidad','hotel')
    list_filter = ('hotel',)
    ordering = ('id',)

admin.site.register(Adicional,Adicional_Admin)
# Register your models here.
