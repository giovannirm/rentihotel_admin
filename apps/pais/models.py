from django.db import models

class Pais(models.Model):
    codigo=models.CharField(verbose_name=u'Código', max_length=10)
    nombre=models.CharField(verbose_name=u'Nombre', max_length=50)

    class Meta:
        verbose_name_plural = "Países"

    def __str__(self):
        return str(self.nombre)