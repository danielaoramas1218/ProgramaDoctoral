from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator



# Create your models here.

class UsuarioManager(BaseUserManager):
    def _create_user(self, email, nombre, apellidos, carnet, sexo, is_casado, password, is_staff, is_superuser,**extra_fields):
        usuario = self.model(
            email = self.normalize_email(email),
            nombre = nombre,
            apellidos = apellidos,
            carnet = carnet,
            is_staff = is_staff,
            is_superuser = is_superuser,
            sexo =sexo,
            is_casado = is_casado,
            **extra_fields
        )
        
        usuario.set_password(password)
        usuario.save(using=self.db)
        return usuario
    
    def create_user(self, email, nombre, apellidos, carnet, sexo = 'E', is_casado = False, password = None,**extra_fields):
        return self._create_user(email,nombre,apellidos, carnet, sexo, is_casado, password, True, False, **extra_fields)
    
    def create_superuser(self, email, nombre, apellidos, carnet, password = None,**extra_fields):
        return self._create_user(email,nombre,apellidos, carnet, 'E', False, password, True, True, **extra_fields)
        

class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Correo', unique=True)
    nombre = models.TextField('Nombre', blank=False, null=False)
    apellidos = models.TextField('Apellidos', blank=False, null=False)
    carnet = models.CharField(max_length=11, null=False)
    pais = models.TextField(null=True)
    titulo = models.TextField(null=True)
    areaTrabajo = models.TextField(null=True)
    sexo = models.CharField(max_length=1, choices=[('M', 'masculino'),('F', 'Femenino'),('E','Especificar')], default='E')
    is_casado = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    fecha_registro = models.DateField(auto_now_add=True)
    objects = UsuarioManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellidos', 'carnet']
    
    def __str__(self):
        return f'{self.nombre},{self.apellidos}'

class Solicitante(models.Model):
    ESTADO = [
        ('P', 'Pendiente'),
        ('C', 'Cancelada')
    ]
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='usuario_solicitante')
    estado = models.CharField(max_length=1, choices=ESTADO, default='P')
    
class Doctor(models.Model):
    nombre = models.TextField('Nombre', blank=False, null=False)
    apellidos = models.TextField('Apellidos', blank=False, null=False)
    email = models.EmailField(null=True)
    carnet = models.CharField(max_length=11, null=False)
    pais = models.TextField(null=True)
    sexo = models.CharField(max_length=1, choices=[('M', 'masculino'),('F', 'Femenino'),('E','Especificar')], default='E')
    is_casado = models.BooleanField(default=False)
    areaPosgrado = models.TextField(null=False)
    fecha_registro = models.DateField(auto_now_add=True)
    
class Doctorando(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='usuario_doctorando')
    tutor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, related_name='doctor_doctorando', null=True)
    tipoTesis = models.TextField(null=True)
    is_master = models.BooleanField(default=False)
    fecha_registro = models.DateField(auto_now_add=True)


