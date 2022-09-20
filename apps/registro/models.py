from django.db import models
from hotel.models import Hotel
from cliente.models import Cliente

class Registro(models.Model):           
    cliente = models.ForeignKey(Cliente,related_name='registro',on_delete=models.SET_NULL, null=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True)   
    reserva = models.IntegerField(verbose_name=u'Reserva', null=True ,blank=True)   # SIN RELACION     
    estado_registro =  models.CharField(max_length=15,verbose_name='Estado Registro')    
    tipo_pago =  models.CharField(max_length=10,verbose_name='Tipo de Pago') 
    adelanto = models.DecimalField(verbose_name='Adelanto', decimal_places=2, max_digits=10)
    precio_total = models.DecimalField(verbose_name='Precio total',decimal_places=2, max_digits=10, null=True, blank=True )
    usuario_registra = models.IntegerField(verbose_name=u'Usuario Registra')
    fecha_registro =  models.DateTimeField(auto_now_add=True , verbose_name=u'Fecha de Registro')  # solo primera vez que se crea el objeto 
    usuario_actualiza = models.IntegerField(verbose_name=u'Usuario Actualiza', null=True ,blank=True)
    fecha_actualiza = models.DateTimeField(auto_now=True , verbose_name=u'Fecha Actualiza') #cada vez que se guarda el objeto

    class Meta:
        verbose_name_plural = "Registros"
    
    def __str__(self):
        return str(self.id)





    

