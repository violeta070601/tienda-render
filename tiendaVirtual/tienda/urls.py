from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'home/roles', views.RolViewSet)
router.register(r'home/clientes', views.ClienteViewSet)
router.register(r'home/vendedores', views.VendedorViewSet)
router.register(r'home/administradores', views.AdministradorViewSet)
router.register(r'home/categorias', views.CategoriaViewSet)
router.register(r'home/productos', views.ProductoViewSet)

urlpatterns = [
    path('', views.loginView, name='login'),
    path('registro-cliente/', views.registro_cliente, name='registro_cliente'),
    path('registro-vendedor/', views.registro_vendedor, name='registro_vendedor'),
    path('', include(router.urls)),
]