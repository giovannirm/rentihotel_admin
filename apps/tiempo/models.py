from django.db import models
from tipohabitacion.models import TipoHabitacion

class Tiempo(models.Model):
    tipo_habitacion = models.ForeignKey(TipoHabitacion, related_name='tiempo', on_delete=models.SET_NULL, null=True)
    codigo = models.CharField(verbose_name=u'Còdigo', max_length=20)
    descripcion = models.TextField(verbose_name=u'Descripciòn', max_length=100,blank=True, null=True)
    valor = models.PositiveIntegerField(verbose_name=u'Valor') # horas
    tipo = models.CharField(verbose_name=u'Tipo', max_length=10)
    precio = models.DecimalField(verbose_name='Precio',decimal_places=2, max_digits=10)
    promocion = models.DecimalField(verbose_name=u'Promoción',decimal_places=2, max_digits=10, blank=True, null=True)
    
        
    def __str__(self):
        return str(self.codigo)

