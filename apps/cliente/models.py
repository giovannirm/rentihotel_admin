from django.db import models

class Cliente (models.Model):
    nombre = models.CharField(max_length=120, verbose_name='Nombres')
    apellido = models.CharField(max_length=120, verbose_name='Apellidos')
    tipo_documento = models.CharField(max_length=10,verbose_name='Tipo Documento')
    numero_documento = models.CharField(max_length=20, verbose_name='N° Documento') # segun el tipo
    genero = models.CharField(max_length=5,verbose_name='Género', null=True, blank=True)
    edad = models.PositiveIntegerField(verbose_name='Edad',null=True, blank=True)
    celular = models.CharField(max_length=30, verbose_name='Nro. Celular')
    correo_electronico = models.CharField(max_length=100, verbose_name='Correo Electronico',null=True, blank=True) 
    nacionalidad = models.IntegerField(verbose_name='Nacionalidad', null=True, blank=True)
    residencia = models.IntegerField(verbose_name='Residencia',null=True, blank=True)
    motivo_viaje = models.IntegerField(verbose_name='Motivo de viaje',null=True, blank=True)
    usuario_registra = models.IntegerField(verbose_name=u'Usuario Registra')
    fecha_registro =  models.DateTimeField(auto_now_add=True , verbose_name=u'Fecha de Registro')
    usuario_actualiza = models.IntegerField(verbose_name=u'Usuario Actualiza',null=True,blank=True)
    fecha_actualiza = models.DateTimeField(auto_now=True , verbose_name=u'Fecha Actualiza')

  
    def __str__(self):
        return str(self.nombre)
