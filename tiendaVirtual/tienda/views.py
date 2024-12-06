from django.shortcuts import render
from rest_framework import viewsets
from .models import Rol, Cliente, Vendedor, Administrador, Categoria, Producto
from .serializers import RolSerializer, ClienteSerializer, VendedorSerializer, AdministradorSerializer, CategoriaSerializer, ProductoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class VendedorViewSet(viewsets.ModelViewSet):
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
        elif hasattr(request.user, 'admin'):
            return redirect('homeAdmin')
        else:
            return redirect('login')  # Si no tiene rol asignado, redirigir al login

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Iniciar sesión del usuario

            # Redirigir al usuario según su rol
            if hasattr(user, 'cliente'):
                return redirect('homeCliente')
            elif hasattr(user, 'vendedor'):
                return redirect('homeVendedor')
            elif hasattr(user, 'admin'):
                return redirect('homeAdmin')
            else:
                return redirect('login')  # Si no tiene rol asignado, redirigir al login
        else:
            messages.error(request, 'Credenciales incorrectas')
            return render(request, 'login.html', {'error': 'Credenciales incorrectas'})

    return render(request, 'login.html')  # Mostrar el formulario de login

def redirect_to_login(request):
    return redirect('login')


@login_required
def inicioCliente(request):
    return render(request, 'cliente/inicioCliente.html')

@login_required
def inicioVendedor(request):
    return render(request, 'vendedor/inicioVendedor.html')

@login_required
def inicioAdmin(request):
    return render(request, 'administrador/inicioAdmin.html')

def registro_cliente(request):
    if request.method == 'POST':    
        pass
    return render(request, 'registros/registroCliente.html')

def registro_vendedor(request):
    if request.method == 'POST':    
        pass
    return render(request, 'registros/registroVendedor.html')

class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [IsAuthenticated]