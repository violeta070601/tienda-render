from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password

class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    aPaterno = models.CharField(max_length=50)
    aMaterno = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10, null=True, blank=True)
    correo = models.EmailField()
    usuario = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)

    def set_password(self, raw_password):
        # Encriptar la contraseña proporcionada por el usuario
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        # Verificar la contraseña proporcionada con la encriptada en la BD
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.nombre
    
class Vendedor(models.Model):
    id_vendedor= models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    aPaterno = models.CharField(max_length=50)
    aMaterno = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10, null=True, blank=True)
    correo = models.EmailField()
    usuario = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)

    def set_password(self, raw_password):
        # Encriptar la contraseña proporcionada por el usuario
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        # Verificar la contraseña proporcionada con la encriptada en la BD
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.nombre

class Administrador(models.Model):
    id_administrador= models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    aPaterno = models.CharField(max_length=50)
    aMaterno = models.CharField(max_length=50)
    correo = models.EmailField()
    usuario = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)

    def set_password(self, raw_password):
        # Encriptar la contraseña proporcionada por el usuario
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        # Verificar la contraseña proporcionada con la encriptada en la BD
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    id_categoria= models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre