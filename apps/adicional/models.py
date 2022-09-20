from django.db import models
from hotel.models import Hotel

class Adicional(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True)
    codigo = models.CharField(verbose_name=u'Código', max_length=10)
    nombre = models.CharField(verbose_name='Nombre', max_length=50)
    cantidad = models.PositiveIntegerField(verbose_name=u'Cantidad')
    estado =  models.CharField(verbose_name='Estado', max_length=50)
    precio = models.DecimalField(verbose_name='Precio', decimal_places=2, max_digits=10)

    def __str__(self):
        return str(self.nombre)