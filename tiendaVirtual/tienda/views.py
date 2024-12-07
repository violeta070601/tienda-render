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