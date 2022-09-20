#from smart_selects.db_fields import ChainedForeignKey
from django.db import models

from pais.models import Pais
from departamento.models import Departamento
from provincia.models import Provincia

class Distrito(models.Model):
    #pais = models.ForeignKey(Pais, on_delete=models.SET_NULL, null=True)
    """
    departamento = ChainedForeignKey(
        Departamento,
        on_delete=models.SET_NULL,
        null=True,
        chained_field="pais",
        chained_model_field="pais",
        show_all=False,        
        )
        
    provincia = ChainedForeignKey(
        Provincia,
        on_delete=models.SET_NULL,
        null=True,
        chained_field="departamento",  
        chained_model_field="departamento", 
        show_all=False,
        )"""

    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True)
    provincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL, null=True)
    codigo = models.CharField(verbose_name=u'Código', max_length=10)
    nombre = models.CharField(verbose_name=u'Nombre', max_length=50)

    def __str__(self):
        return str(self.nombre)