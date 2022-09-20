from django.db import models
from hotel.models import Hotel
from tipohabitacion.models import TipoHabitacion

class Habitacion(models.Model):     
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True)  
    tipo_habitacion = models.ForeignKey(TipoHabitacion, on_delete=models.SET_NULL, null=True) 
    numero_habitacion = models.IntegerField(verbose_name='Nro. Habitacion')
    numero_piso= models.CharField(verbose_name='Nro. Piso', max_length=10, null=True, blank=True)   
    estado_habitacion =  models.CharField(max_length=10,verbose_name='Estado de Habitación')

    class Meta:
        verbose_name_plural = "Habitaciones"

    def __str__(self):
        return str(self.id)


