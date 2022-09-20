from django.db import models
from registrohabitacion.models import RegistroHabitacion

class RegistroAdicional(models.Model):
    registro_habitacion = models.ForeignKey(RegistroHabitacion, related_name='registros_adicional', on_delete=models.SET_NULL, null=True)
    adicional = models.IntegerField(verbose_name=u'Adicional')
    cantidad = models.PositiveIntegerField(verbose_name=u'Cantidad')
    tipo_adicional = models.CharField(verbose_name=u'Tipo Adicional',max_length=10)
    precio_total = models.DecimalField(verbose_name='Precio Total', decimal_places=2, max_digits=10)
       
    class Meta:
        verbose_name_plural = "Registros  Adicional"

   
    def __str__(self):
        return str(self.id)

    
