from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from pais.models import Pais

class MyUserManager(BaseUserManager,):
    def create_user(self, email, password=None,**extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model( email=self.normalize_email(email),**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,password,**extra_fields):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            **extra_fields
		)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Create your models here.
class User(AbstractUser):
    birth_date = models.DateField(verbose_name="Fecha de Nacimiento")
    email = models.EmailField(verbose_name="Correo electrónico", unique=True)
    tipo_usuario = models.CharField(verbose_name=u'Tipo de Usuario',max_length=15)
    pais = models.ForeignKey(Pais,on_delete=models.SET_NULL, null=True ,blank=True)   

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','birth_date','tipo_usuario']

    objects = MyUserManager()

    def __str__(self):
        return self.email