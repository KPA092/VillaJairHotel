from django.shortcuts import render, redirect
from .forms import UserRegistrationForm

def inicio(request):
    # Lógica de la vista de la página de inicio
    return render(request, 'inicio.html', {'section': 'inicio'})

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