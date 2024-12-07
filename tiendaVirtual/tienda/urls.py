from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'home/roles', views.RolViewSet)
router.register(r'home/administradores', views.AdministradorViewSet)
router.register(r'home/categorias', views.CategoriaViewSet)
router.register(r'home/productos', views.ProductoViewSet)

urlpatterns = [
    path('', views.loginView, name='login'),
    path('registro-cliente/', views.registroCliente, name='registroCliente'),
    path('registro-vendedor/', views.RegistroVendedorViewSet.as_view({'post': 'create'}), name='registroVendedor'),
    path('', include(router.urls)),
]