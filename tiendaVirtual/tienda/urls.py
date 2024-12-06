from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'roles', views.RolViewSet)
router.register(r'clientes', views.ClienteViewSet)
router.register(r'vendedores', views.VendedorViewSet)
router.register(r'administradores', views.AdministradorViewSet)
router.register(r'categorias', views.CategoriaViewSet)
router.register(r'productos', views.ProductoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
