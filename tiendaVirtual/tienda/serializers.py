from rest_framework import serializers
from .models import Rol, Usuario, Categoria, Producto

# Serializer para el modelo Rol
class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'nombre']

# Serializer para el modelo Usuario
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            #'id_usuario',
            'nombre',
            'aPaterno',
            'aMaterno',
            'telefono',
            'correo',
            'usuario',
            'rol',
            'is_active',
            'is_staff',
            'is_superuser',
            'password',  # Asegúrate de incluir este campo para la creación del usuario
        ]
        extra_kwargs = {
            'password': {'write_only': True}  # Hacer que la contraseña solo sea de escritura
        }

    def create(self, validated_data):
        from .models import Rol

        # Asegurarse de que el rol "cliente" esté asignado si no se proporciona
        if 'rol' not in validated_data or not validated_data['rol']:
            rol_cliente = Rol.objects.get(nombre="cliente")
            validated_data['rol'] = rol_cliente

        # Forzar los campos is_staff e is_superuser a False
        validated_data['is_active'] = True
        validated_data['is_staff'] = False
        validated_data['is_superuser'] = False

        # Crear el usuario con los datos validados
        user = Usuario.objects.create(**validated_data)

        # Encriptar la contraseña
        if validated_data.get('password', None):
            user.set_password(validated_data['password'])

        # Guardar el usuario en la base de datos
        user.save()

        return user

    

# Serializer para el modelo Categoria
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion']

class ProductoSerializer(serializers.ModelSerializer):
    # Usamos PrimaryKeyRelatedField para solo mostrar el ID de la categoria y usuario
    categoria = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all())
    usuario = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'costo', 'stock', 'categoria', 'usuario']
