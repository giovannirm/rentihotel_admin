from django.db import models
from pais.models import Pais

class Departamento(models.Model):
    pais = models.ForeignKey(Pais, on_delete=models.SET_NULL, null=True)
    codigo = models.CharField(verbose_name=u'Código', max_length=10)
    nombre = models.CharField(verbose_name=u'Nombre', max_length=50)   
    image = models.ImageField(verbose_name='imagen',null=True, blank=True)

    def __str__(self):
        return str(self.nombre)