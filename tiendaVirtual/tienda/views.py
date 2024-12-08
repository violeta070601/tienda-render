from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Rol, Usuario, Categoria, Producto
from .serializers import RolSerializer, UsuarioSerializer, CategoriaSerializer, ProductoSerializer
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.db.models import Count

# ViewSet para el modelo Rol
class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [IsAuthenticated]

# ViewSet para el modelo Usuario
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

# ViewSet para el modelo Categoria
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]

#ViewSet para el modelo Producto
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer



def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Aquí verificamos el rol del usuario y redirigimos según el rol
            if user.rol.nombre == 'administrador':
                return redirect('homeAdmin')  # Redirige al home de administrador
            elif user.rol.nombre == 'vendedor':
                return redirect('homeVendedor')  # Redirige al home de vendedor
            elif user.rol.nombre == 'cliente':
                return redirect('homeCliente')  # Redirige al home de cliente
            else:
                return redirect('login')  # Si no tiene un rol válido, redirige al login

    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def homeAdmin(request):
    return render(request, 'administrador/inicioAdministrador.html', {'user': request.user})
@login_required
def homeVendedor(request):
    return render(request, 'vendedor/inicioVendedor.html', {'user': request.user})
@login_required
def homeCliente(request):
    return render(request, 'cliente/inicioCliente.html', {'user': request.user})

@login_required
def prueba(request):
    return render(request, 'administrador/prueba.html', {'user': request.user})

# Vista para renderizar el formulario de registro
def registro_clientes_view(request):
    return render(request, 'registros/registroCliente.html')

def registro_vendedor_view(request):
    return render(request, 'registros/registroVendedor.html')

# Endpoint para procesar el registro
@api_view(['POST'])
def registrar_cliente(request):
    # Asignar el rol "cliente" directamente en la vista
    rol_cliente = Rol.objects.get(nombre="cliente")  # Obtener el rol "cliente"
    
    # Crear una copia mutable del request.data y añadir el rol
    data = request.data.copy()  # Copiar los datos del request (mutable)
    data['rol'] = rol_cliente.id  # Añadir el rol al diccionario
    
    # Crear el usuario con los datos proporcionados en el request
    serializer = UsuarioSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save()
        return redirect('login')  # Redirige a la vista del login
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def registrar_vendedor(request):
    # Asignar el rol "vendedor" directamente en la vista
    rol_vendedor = Rol.objects.get(nombre="vendedor")  # Obtener el rol "vendedor"
    
    # Crear una copia mutable del request.data y añadir el rol
    data = request.data.copy()  # Copiar los datos del request (mutable)
    data['rol'] = rol_vendedor.id  # Añadir el rol al diccionario
    
    # Crear el usuario con los datos proporcionados en el request
    serializer = UsuarioSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save()
        return redirect('login')  # Redirige a la vista del login
    return Response(serializer.errors, status=400)

def inicioClientesAdmin(request):
    return render(request, 'administrador/clientesAdmin/inicioClientesAdmin.html', {'user': request.user})

def inicioVendedorAdmin(request):
    return render(request, 'administrador/vendedorAdmin/inicioVendedorAdmin.html', {'user': request.user})

def inicioCategoriasAdmin(request):
    return render(request, 'administrador/categoriasAdmin/inicioCategoriasAdmin.html', {'user': request.user})

def inicioProductosAdmin(request):
    return render(request, 'administrador/productosAdmin/inicioProductosAdmin.html', {'user': request.user})

def inicioPedidosAdmin(request):
    return render(request, 'administrador/pedidosAdmin/inicioPedidosAdmin.html', {'user': request.user})
#De aqui para abajo le movi
@login_required
def gestionar_clientes_admin(request):
    # Obtener todos los usuarios con rol de cliente
    clientes = Usuario.objects.filter(rol__nombre="cliente")  # Filtra los usuarios con rol 'cliente'
    
    # Renderizar la página con los clientes
    return render(request, 'administrador/clientesAdmin/gestionarClientesAdmin.html', {'clientes': clientes})
@login_required
def eliminarClientesAdmin(request, cliente_id):
    # Obtener el cliente por id
    cliente = get_object_or_404(Usuario, id=cliente_id)

    if request.method == 'POST':
        # Cambiar el campo is_active a False
        cliente.is_active = False
        cliente.save()
        messages.success(request, f"El cliente {cliente.nombre} ha sido desactivado correctamente.")
        return redirect('gestionarClientesAdmin')  # Redirige a la página de gestión de clientes

    return render(request, 'administrador/clientesAdmin/eliminarClientesAdmin.html', {'cliente': cliente})

def crearCategoriaAdmin(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')

        # Crear la nueva categoría
        categoria = Categoria.objects.create(nombre=nombre, descripcion=descripcion)

        # Mensaje de éxito
        messages.success(request, f"La categoría '{categoria.nombre}' ha sido creada correctamente.")

        return redirect('inicioCategoriasAdmin')  # Redirigir a la página de gestión de categorías

    return render(request, 'administrador/categoriasAdmin/crearCategoriaAdmin.html')  # Mostrar el formulario

@login_required
def gestionarVendedorAdmin(request):
    # Obtener todos los usuarios con rol de cliente
    clientes = Usuario.objects.filter(rol__nombre="vendedor")  # Filtra los usuarios con rol 'cliente'
    
    # Renderizar la página con los clientes
    return render(request, 'administrador/vendedorAdmin/gestionarVendedorAdmin.html', {'clientes': clientes})

def inicioProductosVendedor(request):
    return render(request, 'vendedor/productosVendedor/inicioProductosVendedor.html', {'user': request.user})

def inicioPedidosVendedor(request):
    return render(request, 'vendedor/pedidosVendedor/inicioPedidosVendedor.html', {'user': request.user})


@login_required
def crearProductoVendedor(request):
    # Verificar que el usuario tenga el rol de vendedor
    if request.user.rol.nombre.lower() != 'vendedor':
        # Usar reverse para obtener la URL del login
        login_url = reverse('login')
        return HttpResponseForbidden(f"""
            <h1>Acceso denegado</h1>
            <p>No tienes permisos para realizar esta acción.</p>
            <p><a href="{login_url}">Haz clic aquí para iniciar sesión</a></p>
        """)

    # Procesar el formulario cuando se envíe
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        costo = request.POST.get('costo')
        stock = request.POST.get('stock')
        categoria_id = request.POST.get('categoria')

        # Validar que los campos estén completos
        if not (nombre and descripcion and costo and stock and categoria_id):
            return render(request, 'vendedor/productosVendedor/crearProductoVendedor.html', {
                'categorias': Categoria.objects.all(),
                'error': 'Todos los campos son obligatorios.',
            })

        try:
            # Crear el producto
            categoria = Categoria.objects.get(id=categoria_id)
            Producto.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                costo=costo,
                stock=stock,
                categoria_id=categoria_id,
                usuario_id=request.user.id
            )
            return redirect('inicioProductosVendedor')  # Redirigir a una lista de productos (ajustar según necesidad)
        except Categoria.DoesNotExist:
            return render(request, 'productos/crearProductosVendedor.html', {
                'categorias': Categoria.objects.all(),
                'error': 'La categoría seleccionada no existe.',
            })

    # Si el método es GET, renderizar el formulario
    return render(request, 'vendedor/productosVendedor/crearProductoVendedor.html', {
        'categorias': Categoria.objects.all(),
    })

def gestionarCategoriasAdmin(request):
    # Obtener todas las categorías con el conteo de productos relacionados
    categorias = Categoria.objects.annotate(productos_count=Count('producto'))

    # Renderizar la página con las categorías y el conteo de productos
    return render(request, 'administrador/categoriasAdmin/gestionarCategoriasAdmin.html', {'categorias': categorias})

@login_required
def gestionarProductosAdmin(request):
        #Obtener todas las categorías
        productos = Producto.objects.all()

        #Renderizar la página con las categorías
        return render(request, 'administrador/productosAdmin/gestionarProductosAdmin.html', {'productos': productos})


@login_required
def modificarCategoriasAdmin(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')

        # Actualizar la categoría
        categoria.nombre = nombre
        categoria.descripcion = descripcion
        categoria.save()

        # Mensaje de éxito
        messages.success(request, f"La categoría '{categoria.nombre}' ha sido actualizada correctamente.")

        return redirect('inicioCategoriasAdmin')  # Redirigir a la página de gestión de categorías

    return render(request, 'administrador/categoriasAdmin/modificarCategoriasAdmin.html', {'categoria': categoria})

@login_required
def eliminarCategoriaAdmin(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)

    # Accede a los productos relacionados de la categoría
    productos = categoria.producto_set.all()  # Obtén todos los productos de esa categoría

    if productos.exists():
        # Realiza algo con los productos (por ejemplo, mostrar un mensaje)
        messages.error(request, f"La categoría {categoria.nombre} tiene productos asociados y no puede ser eliminada.")
        return redirect('gestionarCategoriasAdmin')

    if request.method == 'POST':
        categoria.delete()  # Eliminar la categoría
        messages.success(request, f"La categoría '{categoria.nombre}' ha sido eliminada correctamente.")
        return redirect('gestionarCategoriasAdmin')

    return render(request, 'administrador/categoriasAdmin/eliminarCategoriasAdmin.html', {'categoria': categoria})