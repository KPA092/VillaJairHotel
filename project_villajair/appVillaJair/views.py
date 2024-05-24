from django.shortcuts import render, get_object_or_404
from django.http.response import JsonResponse
from .forms import UserRegistrationForm, CustomAuthenticationForm
from .models import Bedrooms, Users, Registers
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseBadRequest
from django.contrib.auth import login as auth_login
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import locale, json
from datetime import datetime
from django.db.models import F

#-----------------------------------------------------HOME------------------------------------------------------
@login_required
def inicio(request):
    return render(request, 'inicio.html', {'section': 'inicio'})

#-------------------------------------------------REGISTRO--------------------------------------------------------
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

#-------------------------------------------------HABITACIONES-------------------------------------------------------
def habitaciones(request):
    habitaciones = Bedrooms.objects.all()
    return render(request, 'habitaciones.html', {'habitaciones': habitaciones})

#----------------------------------------TABLA DE LOS USUARIOS ACTIVOS-----------------------------------------------
def usuariosActivos(request):
    return render(request, 'usuariosActivos.html', {'section': 'usuariosActivos'})

# --------------------------------------OBTENER LOS REGISTROS DEL HISTORIAL------------------------------------------
def historial(request):
    return render(request, 'historial.html')

def listarRegistros(request, user_id):
    registros = Registers.objects.filter(id_user=user_id).annotate(
        bedroom_name=F('id_bedroom__bedroom_name')
    ).values('id_register', 'check_in_date', 'check_out_date', 'bedroom_name')
    data = {'registros': list(registros)}
    return JsonResponse(data)

# --------------------------------------------TABLA DE TODOS LOS USUARIOS---------------------------------------------
def todosLosUsuarios(request):
    return render(request, 'todosLosUsuarios.html', {'section': 'todosLosUsuarios'})

def listarTodosLosUsuarios(request):
    users = list(Users.objects.values())
    data = {'users': users}
    return JsonResponse(data)

def listarUsuariosPorMes(request, year, month):
    year = int(year)
    month = int(month)
    registers_for_month = Registers.objects.filter(check_in_date__year=year, check_in_date__month=month)
    users_for_month = Users.objects.filter(id_user__in=registers_for_month.values_list('id_user', flat=True))
    users_data = list(users_for_month.values())
    return JsonResponse({'users': users_data})

def get_user(request, user_id):
    user = get_object_or_404(Users, id_user=user_id)
    user_data = {
        'id': user.id_user,
        'full_name': user.full_name,
        'email': user.email,
        'phone_number': user.phone_number,
        'age': user.age,
        'country': user.country,
    }
    return JsonResponse(user_data)

def updateUser(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(Users, id_user=user_id)
        data = json.loads(request.body)
        user.full_name = data['full_name']
        user.email = data['email']
        user.phone_number = data['phone_number']
        user.age = data['age']
        user.country = data['country']
        # Actualiza el campo update_at con la fecha y hora actuales
        user.updated_at = timezone.now()
        user.save()
        return HttpResponse(status=200)
    return HttpResponse(status=405)

#-------------------------------------------DESCARGAR PDF TODOS-------------------------------------------------
def download_all_users_pdf(request):
    data = get_all_users_data_for_pdf()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="registros_todos_usuarios.pdf"'
    generate_all_users_pdf(data, response)
    return response

def get_all_users_data_for_pdf():
    registers = Registers.objects.all()
    registros = []

    for registro in registers:
        user_data = Users.objects.get(id_user=registro.id_user_id)
        registro_info = {
            'full_name': user_data.full_name,
            'nit': user_data.nit,
            'email': user_data.email,
            'phone_number': user_data.phone_number,
            'age': user_data.age,
            'country': user_data.country,
            'check_in_date': registro.check_in_date,
            'check_out_date': registro.check_out_date
        }
        registros.append(registro_info)

    return registros

def generate_all_users_pdf(data, response):
    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    # Título del PDF
    title = Paragraph('Todos los Usuarios', title_style)
    # Configura los datos de la tabla para el PDF
    table_data = [['Nombre', 'NIT', 'Email', 'Teléfono', 'Edad', 'País', 'Fecha Entrada', 'Fecha Salida']]
    for registro in data:
        table_data.append([
            registro['full_name'],
            registro['nit'],
            registro['email'],
            registro['phone_number'],
            registro['age'],
            registro['country'],
            registro['check_in_date'].strftime("%Y-%m-%d %H:%M:%S"),
            registro['check_out_date'].strftime("%Y-%m-%d %H:%M:%S") if registro['check_out_date'] else ''
        ])
    table = Table(table_data)
    table.setStyle(table_style)

    elements = [title, Spacer(1, 0.2 * inch), table]
    doc.build(elements)

# --------------------------------------------DESCARGAR PDF MES-----------------------------------------------------
def download_pdf(request):
    selected_month = request.GET.get('selected_month')
    data = get_data_for_pdf(selected_month)
    if not data:
        return HttpResponseBadRequest('No hay registros para este mes')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="registros_{selected_month}.pdf"'
    generate_pdf(data, response, selected_month)
    return response

def get_data_for_pdf(selected_month):
    selected_month = int(selected_month)
    registers = Registers.objects.filter(check_in_date__month=selected_month)
    registros = []
    for registro in registers:
        user_data = Users.objects.get(id_user=registro.id_user_id)
        registro_info = {
            'full_name': user_data.full_name,
            'nit': user_data.nit,
            'email': user_data.email,
            'phone_number': user_data.phone_number,
            'age': user_data.age,
            'country': user_data.country,
            'check_in_date': registro.check_in_date,
            'check_out_date': registro.check_out_date
        }
        registros.append(registro_info)

    return registros

def generate_pdf(data, response, month):
    doc = SimpleDocTemplate(response, pagesize=letter)
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    month_name = datetime.strptime(month, "%m").strftime("%B").capitalize()
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    # Título del PDF
    title = Paragraph(f'Registros del mes: {month_name}', title_style)
    # Configura los datos de la tabla para el PDF
    table_data = [['Nombre', 'NIT', 'Email', 'Teléfono', 'Edad', 'País', 'Fecha Entrada', 'Fecha Salida']]
    for registro in data:
        table_data.append([
            registro['full_name'],
            registro['nit'],
            registro['email'],
            registro['phone_number'],
            registro['age'],
            registro['country'],
            registro['check_in_date'].strftime("%Y-%m-%d %H:%M:%S"),
            registro['check_out_date'].strftime("%Y-%m-%d %H:%M:%S") if registro['check_out_date'] else ''
        ])
    table = Table(table_data)
    table.setStyle(table_style)
    elements = [title, Spacer(1, 0.2 * inch), table]
    doc.build(elements)

# --------------------------------------------------LOGIN-----------------------------------------------------------
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

#-----------------------------------------------------LOGOUT----------------------------------------------------------
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('login'))  # Redirige a la página de inicio de sesión
