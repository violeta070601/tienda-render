from django import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RolViewSet, UsuarioViewSet, CategoriaViewSet
from . import views

router = DefaultRouter()

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('homeAdmin/', views.homeAdmin, name='homeAdmin'),
    path('homeVendedor/', views.homeVendedor, name='homeVendedor'),
    path('homeCliente/', views.homeCliente, name='homeCliente'),
    path('prueba/', views.prueba, name='prueba'),
    path('super/', include(router.urls)),
]