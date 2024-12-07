from django import forms
from .models import Cliente
from django.contrib.auth.forms import UserCreationForm

# Crear un formulario de cliente
class ClienteForm(UserCreationForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'aPaterno', 'aMaterno', 'telefono', 'correo', 'usuario', 'password']