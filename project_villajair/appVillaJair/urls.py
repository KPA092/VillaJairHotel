from . import views
from django.urls import path

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('habitaciones/', views.habitaciones, name='habitaciones'),
    path('usuariosActivos/', views.usuariosActivos, name='usuariosActivos'),
    path('todosLosUsuarios/', views.todosLosUsuarios, name='todosLosUsuarios'),
]