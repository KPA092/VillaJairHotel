from . import views
from django.urls import path
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('inicio/', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('habitaciones/', views.habitaciones, name='habitaciones'),
    path('usuariosActivos/', views.usuariosActivos, name='usuariosActivos'),
    path('todosLosUsuarios/', views.todosLosUsuarios, name='todosLosUsuarios'),
    path('', views.login, name='login'),    
    path('logout/', views.logout, name='logout'),
    #Forgot password
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]