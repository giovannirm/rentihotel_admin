from django.db import models

class RegistroCliente(models.Model):
    nombre = models.CharField(max_length=120, verbose_name='Nombres')
    apellido = models.CharField(max_length=120, verbose_name='Apellidos')
    tipo_documento = models.CharField(max_length=10, verbose_name='Tipo Documento')
    numero_documento = models.CharField(max_length=20, verbose_name='N° Documento') # segun el tipo
    genero = models.CharField(max_length=5,verbose_name='Género')
    edad = models.PositiveIntegerField(verbose_name='Edad')
    celular = models.CharField(max_length=15, verbose_name='Nro. Celular')
    correo_electronico = models.CharField(max_length=100, verbose_name='Correo Electrónico')
    tipo_cliente = models.CharField(max_length=10,verbose_name='Tipo Cliente')  #logueado o no
    fecha_registro = models.DateTimeField(auto_now_add=True , verbose_name=u'Fecha de Resgistro')

    class Meta:
        verbose_name_plural = "Registro de Clientes"

    def __str__(self):
        #return str(self.numero_documento)
        return str(self.nombre)
