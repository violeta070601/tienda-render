from rest_framework import serializers
from .models import Rol, Cliente, Vendedor, Administrador, Categoria, Producto

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id_cliente', 'nombre', 'aPaterno', 'aMaterno', 'telefono', 'correo', 'usuario', 'password']

    def create(self, validated_data):
        validated_data['rol_id'] = 3

        # Crear el cliente sin la contraseña encriptada
        cliente = Cliente(**validated_data)
        
        
        # Llamar al método set_password para encriptar la contraseña antes de guardarla
        cliente.set_password(validated_data['password'])

        # Guardar el cliente en la base de datos
        cliente.save()
        return cliente

class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        exclude = ['rol']

    def create(self, validated_data):
        validated_data['rol_id'] = 2
        # Crear el vendedor sin la contraseña encriptada
        vendedor = Vendedor(**validated_data)

        # Llamar al método set_password para encriptar la contraseña antes de guardarla
        vendedor.set_password(validated_data['password'])

        # Guardar el vendedor en la base de datos
        vendedor.save()
        return vendedor

class AdministradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrador
        fields = '__all__'

    def create(self, validated_data):
        # Crear el administrador sin la contraseña encriptada
        administrador = Administrador(**validated_data)

        # Llamar al método set_password para encriptar la contraseña antes de guardarla
        administrador.set_password(validated_data['password'])

        # Guardar el administrador en la base de datos
        administrador.save()
        return administrador

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer()  # Puedes incluir la categoría en el Producto
    class Meta:
        model = Producto
        fields = '__all__'
