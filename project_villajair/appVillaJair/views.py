from django.shortcuts import render, redirect
from .forms import UserRegistrationForm,CustomAuthenticationForm
from .models import Bedrooms, States
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages



@login_required
def inicio(request):
    return render(request, 'inicio.html', {'section': 'inicio'})

@login_required
def registro(request):
    if request.method == 'POST':
        form =  UserRegistrationForm(request.POST)
        if form.is_valid():
            # Lógica para procesar el formulario
            # Por ejemplo, guardar los datos en la base de datos
            form.save()
            # Redirigir a una página de éxito o a otra URL

    else:
        form =  UserRegistrationForm()
    return render(request, 'registro.html', {'form': form, 'section': 'registro'})

def habitaciones(request):
    habitaciones = Bedrooms.objects.all()
    estados = States.objects.filter(id_type_state=2)
    
    return render(request, 'habitaciones.html', {'habitaciones': habitaciones, 'estados': estados})

def guardar_cambios(request):
    if request.method == 'POST':
        # Obtener el ID de la habitación y el nuevo estado enviado desde el formulario
        habitacion_id = request.POST.get('habitacion_id')
        nuevo_estado_id = request.POST.get('estado_habitacion')
        
        # Obtener la habitación y el nuevo estado de la base de datos
        habitacion = Bedrooms.objects.get(id_bedroom=habitacion_id)
        nuevo_estado = States.objects.get(id_state=nuevo_estado_id)
        
        # Actualizar el estado de la habitación
        habitacion.id_state = nuevo_estado
        habitacion.save()
        
    return redirect('habitaciones')

def usuariosActivos(request):
    return render(request, 'usuariosActivos.html', {'section': 'usuariosActivos'})

def todosLosUsuarios(request):
    return render(request, 'todosLosUsuarios.html', {'section': 'todosLosUsuarios'})

    return render(request, 'registro.html', {'form': form, 'section': 'registro'})


def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return HttpResponseRedirect(reverse('inicio'))  # Redirige a la página de inicio
        else:
            username = form.cleaned_data.get('username')
            if username:
                if request.session.get('login_attempts', 0) >= 5:
                    # Puedes implementar la lógica para bloquear la IP aquí
                    pass
                else:
                    request.session['login_attempts'] = request.session.get('login_attempts', 0) + 1
           
            form = CustomAuthenticationForm()
         
            messages.error(request, "Credenciales incorrectas. Inténtalo de nuevo.")
            return render(request, 'login.html', {'form': form})
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('login'))  # Redirige a la página de inicio de sesión
