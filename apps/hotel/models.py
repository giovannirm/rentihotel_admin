from django.db import models
#from smart_selects.db_fields import ChainedForeignKey
from pais.models import Pais
from departamento.models import Departamento
from provincia.models import Provincia
from distrito.models import Distrito
from usuario.models import User

def file_name(instance, filename):  
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename> 
    #print(instance.id)
    return '{0}_{1}'.format(instance.id, filename) 
   
class Hotel(models.Model): 
    pais = models.ForeignKey(Pais, on_delete=models.SET_NULL, null=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True)
    provincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL, null=True)
    distrito = models.ForeignKey(Distrito, on_delete=models.SET_NULL, null=True)
    usuarios = models.ManyToManyField(User,verbose_name=('usuarios'),blank=True,)    
    nombre= models.CharField(max_length=200, verbose_name='Nombre')
    ruc = models.CharField(max_length=20, verbose_name='RUC', blank=True, null=True)
    direccion= models.CharField(max_length=120, verbose_name='Direccion')
    descripcion = models.TextField(verbose_name='Breve Descripciòn')
    total_habitacion = models.PositiveIntegerField(verbose_name='Total Habitaciones')
    telefono = models.CharField(max_length=30, verbose_name='Nro. Telefono', blank=True, null=True)
    celular = models.CharField(max_length=30, verbose_name='Nro. Celular')
    correo_electronico = models.CharField(max_length=100, verbose_name='Correo Electronico')
    cochera = models.BooleanField(verbose_name='Tiene Cochera')
    tarjeta = models.BooleanField(verbose_name='Acepta Tarjeta')
    latitud = models.CharField(max_length=100, verbose_name='Latitud')
    longitud = models.CharField(max_length=100, verbose_name='Longitud')
    webpage = models.CharField(max_length=100, verbose_name='Pagina Web')
    logo = models.ImageField(verbose_name='Logo', null=True, blank=True, upload_to = file_name)
    fanpage = models.CharField(max_length=200, verbose_name=u'Fan Page', null=True, blank=True)
    instagram = models.CharField(max_length=200, verbose_name='Instagram', null=True, blank=True)    
    image1 = models.ImageField(verbose_name='imagen1')  #max_length=None
    image2 = models.ImageField(verbose_name='imagen2',null=True, blank=True)
    image3 = models.ImageField(verbose_name='imagen3',null=True, blank=True)
    clasificacion = models.IntegerField(verbose_name='Nro. Estrellas')
    clase = models.CharField(max_length=30, verbose_name='Clase', null=True, blank=True)

    
   
    
    '''     
    departamento = ChainedForeignKey(
        Departamento,
        on_delete=models.SET_NULL,
        null=True,
        chained_field="pais",  #con cual quieres encadenar  dentro de tu propio modelo 
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
    )
  
    distrito = ChainedForeignKey(
        Distrito,
        on_delete=models.SET_NULL,
        null=True,
        chained_field="provincia",  
        chained_model_field="provincia", 
        show_all=False,
    )
    '''    
    
    #usuarioregistro = models.ForeignKey(User, on_delete=models.SET_NULL, null=True )
    
    class Meta:
        verbose_name_plural = "Hoteles"

    def __str__(self):
        return str(self.nombre)
