from django.db import models
from tipohabitacion.models import TipoHabitacion

class Servicio(models.Model):        
    tipo_habitacion = models.ForeignKey(TipoHabitacion, related_name='servicio', on_delete=models.SET_NULL, null=True )    
    codigo = models.CharField(max_length=100, verbose_name='Codigo')
    nombre = models.CharField(max_length=100, verbose_name='Nombre')

    def __str__(self):
        return str(self.nombre)