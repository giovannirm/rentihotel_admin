from django.utils import timezone
from django.db import models

from hotel.models import Hotel
from habitacion.models import Habitacion
from tipohabitacion.models import TipoHabitacion
from tiempo.models import Tiempo
from registrocliente.models import RegistroCliente
from utils.utils import random_code

class Reserva(models.Model):
    #hour = timezone.now()
    #formatedHour = hour.strftime("%H:%M:%S")
    #default=formatedHour

    registro_cliente = models.ForeignKey(RegistroCliente,related_name='reserva',on_delete=models.SET_NULL, null=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True)      
    fecha_ingreso = models.DateField(verbose_name=u'Fecha de Ingreso')
    fecha_salida = models.DateField(verbose_name=u'Fecha de Salida',blank=True, null=True)
    hora_llegada = models.CharField(max_length=10,verbose_name=u'Hora de llegada',)
    estado_reserva =  models.CharField(max_length=10, verbose_name='Estado Reserva')    # parametros int
    codigo_reserva =  models.CharField(max_length=6, verbose_name=u'Código Reserva' , default=str(random_code(6)))  
 
    cantidad_adulto = models.IntegerField(verbose_name=u'Cantidad de Adultos',blank=True, null=True)
    cantidad_nino = models.IntegerField(verbose_name=u'Cantidad de Niños',blank=True, null=True)

    subtotal = models.DecimalField(verbose_name='Subtotal', decimal_places=2, max_digits=10) 
    igv = models.DecimalField(verbose_name='IGV', decimal_places=2, max_digits=10) 
    precio_total = models.DecimalField(verbose_name='Precio total', decimal_places=2, max_digits=10) 

    tipo_pago =  models.CharField(max_length=10,verbose_name='Tipo de Pago')  # parametros int
    adelanto = models.DecimalField(verbose_name='Adelanto', decimal_places=2, max_digits=10)
      
    fecha_registro =  models.DateTimeField(auto_now_add=True , verbose_name=u'Fecha de Registro')  # solo primera vez que se crea el objeto 

    def __str__(self):
        return str(self.id)
# Create your models here.
