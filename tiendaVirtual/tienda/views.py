from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Rol, Usuario, Categoria
from .serializers import RolSerializer, UsuarioSerializer, CategoriaSerializer
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status

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
