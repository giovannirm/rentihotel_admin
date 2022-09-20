from django.db import models

class Parametro(models.Model):
    grupo = models.CharField(verbose_name=u'Grupo', max_length=30)
    codigo = models.CharField(verbose_name=u'Código', max_length=10)
    nombre = models.CharField(verbose_name='Nombre', max_length=50)
    descripcion = models.TextField(verbose_name=u'Descripción', max_length=500, null=True, blank=True)  
    valor = models.IntegerField(verbose_name=u'Valor',null=True,blank=True)    
    estado = models.CharField(verbose_name=u'Estado', max_length=10)
    usuario_registra = models.IntegerField(verbose_name=u'Usuario Registra')
    fecha_registro =  models.DateTimeField(auto_now_add=True , verbose_name=u'Fecha de Registro')  # solo primera vez que se crea el objeto 
    usuario_actualiza = models.IntegerField(verbose_name=u'Usuario Actualiza',null=True,blank=True)
    fecha_actualiza = models.DateTimeField(auto_now=True , verbose_name=u'Fecha Actualiza') #cada vez que se guarda el objeto

    def __str__(self):
        return str(self.nombre)
