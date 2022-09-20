from django.db import models

class PagoCulqi(models.Model):
    registro_cliente = models.IntegerField(verbose_name='Registro Cliente')
    reserva = models.IntegerField(verbose_name='Reserva')
    cargo = models.CharField(max_length=80, verbose_name='Cargo')
    fecha_registro =  models.DateTimeField(auto_now_add=True , verbose_name=u'Fecha de Registro')

    class Meta:
        verbose_name_plural = "Pagos Culqi"

    def __str__(self):
        return str(self.id)
