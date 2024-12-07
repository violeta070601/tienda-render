from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import ClienteForm
from .models import Rol, Cliente, Vendedor, Administrador, Categoria, Producto
from .serializers import RolSerializer, ClienteSerializer, VendedorSerializer, AdministradorSerializer, CategoriaSerializer, ProductoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from .serializers import ClienteSerializer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
    
class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer

class RegistroClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class RegistroVendedorViewSet(viewsets.ModelViewSet):
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer

class AdministradorViewSet(viewsets.ModelViewSet):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

#Vista del login
def loginView(request):
    # Verificar si el usuario ya está autenticado
    if request.user.is_authenticated:
        # Redirigir según el rol del usuario
        if hasattr(request.user, 'cliente'):
            return redirect('homeCliente')
        elif hasattr(request.user, 'vendedor'):
            return redirect('homeVendedor')
        elif hasattr(request.user, 'administrador'):
            return redirect('homeAdmin')
        else:
            return redirect('login')  # Si no tiene rol asignado, redirigir al login

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            # Buscar al usuario manualmente en la base de datos
            user = None
            if Cliente.objects.filter(usuario=username).exists():
                user = Cliente.objects.get(usuario=username)
            elif Vendedor.objects.filter(usuario=username).exists():
                user = Vendedor.objects.get(usuario=username)
            elif Administrador.objects.filter(usuario=username).exists():
                user = Administrador.objects.get(usuario=username)
            
            if user:
                # Verificar la contraseña usando check_password
                if user.check_password(password):
                    # Iniciar sesión del usuario manualmente
                    if isinstance(user, Cliente):
                        request.session['user_id'] = user.id_cliente  # Usar el ID específico para Cliente
                    elif isinstance(user, Vendedor):
                        request.session['user_id'] = user.id_vendedor  # Usar el ID específico para Vendedor
                    elif isinstance(user, Administrador):
                        request.session['user_id'] = user.id_administrador  # Usar el ID específico para Administrador
                    
                    # Redirigir según el rol del usuario
                    if isinstance(user, Cliente):
                        print(f"Usuario {user.usuario} ha iniciado sesión como cliente.")  # Depuración
                        return render(request, 'cliente/inicioCliente.html', {'usuario_nombre': user.usuario, 'usuario_id': user.id_cliente})
                    elif isinstance(user, Vendedor):
                        return render(request, 'vendedor/inicioVendedor.html', {'usuario_nombre': user.usuario, 'usuario_id': user.id_vendedor})
                    elif isinstance(user, Administrador):
                        return render(request, 'administrador/inicioAdministrador.html', {'usuario_nombre': user.usuario, 'usuario_id': user.id_administrador})
                else:
                    messages.error(request, 'Credenciales incorrectas')
                    return render(request, 'login.html', {'error': 'Credenciales incorrectas'})
            else:
                messages.error(request, 'Usuario no encontrado')
                return render(request, 'login.html', {'error': 'Usuario no encontrado'})
        except Exception as e:
            messages.error(request, 'Hubo un error al intentar iniciar sesión')
            return render(request, 'login.html', {'error': str(e)})

    return render(request, 'login.html')  # Mostrar el formulario de login





def redirect_to_login(request):
    return redirect('login')


def homeCliente(request):
    return render(request, 'cliente/inicioCliente.html')


def homeVendedor(request):
    return render(request, 'vendedor/inicioVendedor.html')


def homeAdmin(request):
    return render(request, 'administrador/inicioAdministrador.html')

def registroCliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()  # Guardar el cliente en la base de datos
            messages.success(request, 'Cliente registrado exitosamente')
            return HttpResponseRedirect('/login')  # Redirigir al login
    
    return render(request, 'registros/registroCliente.html')


class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [IsAuthenticated]