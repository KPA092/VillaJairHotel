from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('inicio/', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('habitaciones/', views.habitaciones, name='habitaciones'),
    path('usuariosActivos/', views.usuariosActivos, name='usuariosActivos'),

    # -----------------------------------------URLS DE TODOS LOS USUARIOS-----------------------------------------------
    path('todosLosUsuarios/', views.todosLosUsuarios, name='todosLosUsuarios'),
	path('listarTodosLosUsuarios/', views.listarTodosLosUsuarios, name='listarTodosLosUsuarios'),
	path('listarUsuariosPorMes/<int:year>/<int:month>/', views.listarUsuariosPorMes, name='listar_usuarios_por_mes'),
    path('get_user/<int:user_id>/', views.get_user, name='get_user'),
    path('updateUser/<int:user_id>/', views.updateUser, name='updateUser'),

    #-----------------------------------------------HISTORIAL DE REGISTROS----------------------------------------------
	path('historial/', views.historial, name='historial'),
    path('listarRegistros/<int:user_id>', views.listarRegistros, name='listarRegistros'),

    # -----------------------------------------------DESCARGAR PDF------------------------------------------------------
	path('descargar_pdf/', views.download_pdf, name='download_pdf'),
	path('download_all_users_pdf/', views.download_all_users_pdf, name='download_all_users_pdf'),

    # ------------------------------------------------LOGIN, LOGOUT----------------------------------------------------
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    # -------------------------------------------------FORGOT PASSWORD--------------------------------------------------
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]