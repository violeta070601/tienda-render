from django.contrib import admin
from .models import Rol, Cliente, Vendedor, Administrador, Categoria, Producto

# Registra los modelos
admin.site.register(Rol)
admin.site.register(Cliente)
admin.site.register(Vendedor)
admin.site.register(Administrador)
admin.site.register(Categoria)
admin.site.register(Producto)