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
    
# Modelo Productos
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Relación con el usuario que da de alta

    def __str__(self):
        return self.nombre
    
# Modelo Carrito
class Carrito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='carritos')  # Relación con Usuario
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    updated_at = models.DateTimeField(auto_now=True)  # Fecha de última actualización

    def __str__(self):
        return f"Carrito de {self.usuario.usuario} ({self.id})"

    def get_total_price(self):
        """Calcula el precio total del carrito."""
        return sum(item.get_total_price() for item in self.items.all())

    def clear_cart(self):
        """Vacía el carrito."""
        self.items.all().delete()

# Modelo CarritoItems (Elementos dentro del carrito)
class CarritoItems(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')  # Relación con Carrito
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Relación con Producto
    cantidad = models.PositiveIntegerField(default=1)  # Cantidad de productos en el carrito

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Carrito ID: {self.carrito.id})"

    def get_total_price(self):
        """Obtiene el precio total para este elemento del carrito."""
        return self.producto.costo * self.cantidad