from django import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RolViewSet, UsuarioViewSet, CategoriaViewSet
from . import views

router = DefaultRouter()

urlpatterns = [
    path('', views.login_view, name='login'),                                               #Esta es la ruta para el login
    path('logout/', views.logout_view, name='logout'),                                      #Esta es la ruta para que se pueda cerrar sesion, va en todas las putas vistas de html que usen
    path('homeAdmin/', views.homeAdmin, name='homeAdmin'),                                  #Pagina de inicio para el administrador de la tienda
    path('homeVendedor/', views.homeVendedor, name='homeVendedor'),                         #Pagina de inicio para el vendedor de la tienda
    path('homeCliente/', views.homeCliente, name='homeCliente'),                            #Pagina de inicio para el cliente de la tienda
    path('prueba/', views.prueba, name='prueba'),                                           #A esto no le muevan bola de nacos
    path('registroCliente/', views.registro_clientes_view, name='registro_clientes'),       #URL para entrar al registro de clientes
    path('api/registrar_cliente/', views.registrar_cliente, name='registrar_cliente'),      #URL para dar de alta al cliente
    path('registroVendedor/', views.registro_vendedor_view, name='registro_vendedor'),
    path('api/registrar_vendedor/', views.registrar_vendedor, name='registrar_vendedor'),
    path('inicioClientesAdmin/', views.inicioClientesAdmin, name='inicioClientesAdmin'),
    path('inicioVendedorAdmin/', views.inicioVendedorAdmin, name='inicioVendedorAdmin'),
    path('inicioCategoriasAdmin/', views.inicioCategoriasAdmin, name='inicioCategoriasAdmin'),
    path('inicioProductosAdmin/', views.inicioProductosAdmin, name='inicioProductosAdmin'),
    path('inicioPedidosAdmin/', views.inicioPedidosAdmin, name='inicioPedidosAdmin'),  
    path('super/', include(router.urls)),
    path('gestionarClientesAdmin/', views.gestionar_clientes_admin, name='gestionarClientesAdmin'),
    path('eliminarClientesAdmin/<int:cliente_id>/', views.eliminarClientesAdmin, name='eliminarClientesAdmin'),
    path('crearCategoriaAdmin/', views.crearCategoriaAdmin, name='crearCategoriaAdmin'),
    path('gestionarCategoriasAdmin/', views.gestionarCategoriasAdmin, name='gestionarCategoriasAdmin'),
    path('gestionarVendedorAdmin/', views.gestionarVendedorAdmin, name='gestionarVendedorAdmin'),
    path('inicioProductosVendedor/', views.inicioProductosVendedor, name='inicioProductosVendedor'),
    path('inicioPedidosVendedor/', views.inicioPedidosVendedor, name='inicioPedidosVendedor'),
    path('crearProductoVendedor/', views.crearProductoVendedor, name='crearProductoVendedor'),
    path('gestionarProductosAdmin/', views.gestionarProductosAdmin, name='gestionarProductosAdmin'),
]