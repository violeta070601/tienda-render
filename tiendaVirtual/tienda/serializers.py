from rest_framework import serializers
from .models import Rol, Usuario, Categoria

# Serializer para el modelo Rol
class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'nombre']

# Serializer para el modelo Usuario
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id_usuario', 'nombre', 'aPaterno', 'aMaterno', 'telefono', 'correo', 'usuario', 'rol', 'is_active', 'is_staff', 'is_superuser']

# Serializer para el modelo Categoria
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id_categoria', 'nombre', 'descripcion']
