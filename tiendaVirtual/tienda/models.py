from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager

# Modelo de Rol
class Rol(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

# Crear el manager para el usuario
class UsuarioManager(BaseUserManager):
    def create_user(self, correo, usuario, password=None, **extra_fields):
        if not correo:
            raise ValueError('El correo debe ser proporcionado')
        correo = self.normalize_email(correo)
        # Crear el usuario
        user = self.model(correo=correo, usuario=usuario, **extra_fields)
        
        if password:
            user.set_password(password)  # Encriptar la contraseña
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, usuario, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(correo, usuario, password, **extra_fields)

# Modelo Usuario personalizado
class Usuario(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=50)
    aPaterno = models.CharField(max_length=50)
    aMaterno = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10, null=True, blank=True)
    correo = models.EmailField(unique=True)
    usuario = models.CharField(max_length=100, unique=True)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Para permisos de admin
    is_superuser = models.BooleanField(default=False)

    # Usar el manager personalizado
    objects = UsuarioManager()

    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = ['correo', 'nombre', 'aPaterno', 'aMaterno']

    def __str__(self):
        return self.usuario

# Modelo Categoria
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre