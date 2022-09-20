from django.db import models
from hotel.models import Hotel
#from tiempo.models import Tiempo

class TipoHabitacion(models.Model):
    hotel = models.ForeignKey(Hotel,related_name='tipo_habitacion',on_delete=models.SET_NULL, null=True)  
    nombre = models.CharField(verbose_name='Nombre', max_length=20)
    descripcion = models.TextField(verbose_name=u'Descripciòn', max_length=100, null=True, blank=True)   
    foto_uno  = models.ImageField(verbose_name='Imagen 1')
    foto_dos  = models.ImageField(verbose_name='Imagen 2',null=True, blank=True)
    foto_tres = models.ImageField(verbose_name='Imagen 3',null=True, blank=True)
    capacidad_persona = models.PositiveIntegerField(verbose_name=u'Capacidad máxima de personas')
    

    # jalar precio del tiempo es dinamico en el serializador   
  
    class Meta:
        verbose_name_plural = "Tipo de Habitaciones"

    def __str__(self):
        return str(self.id)




