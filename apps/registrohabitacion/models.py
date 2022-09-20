from django.db import models

from registro.models import Registro
from hospedante.models import Hospedante

class RegistroHabitacion(models.Model):
    registro = models.ForeignKey(Registro,related_name='registros_habitacion', on_delete=models.SET_NULL, null=True)   
    hospedantes = models.ManyToManyField(Hospedante,verbose_name=('hospedantes'),blank=True,)  
    
    habitacion = models.IntegerField(verbose_name=u'Habitacion')
    estado_habitacion =  models.CharField(max_length=15,verbose_name='Estado Habitación')
    fecha_ingreso = models.DateTimeField(verbose_name=u'Fecha de Ingreso')
    fecha_salida = models.DateTimeField(verbose_name=u'Fecha de Salida')
    codigo = models.CharField(max_length=15,verbose_name='Código')
    tiempo = models.IntegerField(verbose_name=u'Tiempo')
    cantidad_adulto = models.IntegerField(verbose_name=u'Cantidad de Adultos')
    cantidad_nino = models.IntegerField(verbose_name=u'Cantidad de niños')

    precio = models.DecimalField(verbose_name='Precio',decimal_places=2, max_digits=10)
    precio_total  = models.DecimalField(verbose_name='Precio Total', decimal_places=2, max_digits=10 ,null=True, blank=True ) 

    usuario_registra = models.IntegerField(verbose_name=u'Usuario Registra')
    fecha_registro =  models.DateTimeField(auto_now_add=True , verbose_name=u'Fecha de Registro')  # solo primera vez que se crea el objeto 
    usuario_actualiza = models.IntegerField(verbose_name=u'Usuario Actualiza', null=True ,blank=True)
    fecha_actualiza = models.DateTimeField(auto_now=True , verbose_name=u'Fecha Actualiza') #cada vez que se guarda el objeto

    def __str__(self):
        return str(self.id)