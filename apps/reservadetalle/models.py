from django.db import models
from reserva.models import Reserva

class ReservaDetalle(models.Model):
    reserva = models.ForeignKey(Reserva, related_name='reserva_detalle',on_delete=models.SET_NULL, null=True)
    tipo_habitacion =  models.IntegerField(verbose_name='Tipo Habitación') 
    precio_total  = models.DecimalField(verbose_name='Precio Total', decimal_places=2, max_digits=10)
    tiempo = models.IntegerField(verbose_name=u'Tiempo')
    cantidad = models.IntegerField(verbose_name=u'Cantidad')
    fecha_registro =  models.DateTimeField(auto_now_add=True , verbose_name=u'Fecha de Registro')

    class Meta:
        verbose_name_plural = "Registros de Reserva Detalle"

    def __str__(self):
        #return "{} - {}".format(self.reserva,self.tipo_habitacion)
        return str(self.id)