from django.shortcuts import render, get_object_or_404
from django.http.response import JsonResponse
from .forms import UserRegistrationForm, CustomAuthenticationForm, RegisterForm
from .models import Bedrooms, Users, Registers
from django.shortcuts import render
from .forms import UserRegistrationForm,CustomAuthenticationForm
from .models import Bedrooms, States, Users, Registers
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
from django.http import Http404

#-----------------------------------------------------HOME------------------------------------------------------
from django.http import JsonResponse
from PIL import Image
from PIL import UnidentifiedImageError
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys, os
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
from .tasks import iniciar_tarea_actualizacion

# Variable para asegurar que la tarea se inicia solo una vez
tarea_iniciada = False
MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024  # Tamaño máximo permitido en bytes (10 MB)


@login_required
def inicio(request):
    global tarea_iniciada
    if not tarea_iniciada:
        iniciar_tarea_actualizacion()
        tarea_iniciada = True
    return render(request, 'inicio.html')

#-------------------------------------------------REGISTRO--------------------------------------------------------
@login_required
def registro(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            nit = form.cleaned_data.get('nit')
            edad = form.cleaned_data.get('age')
            edad_minima = 18  
            
            # Verifica si el usuario ya existe
            try:
                user = Users.objects.get(nit=nit)
                if request.POST.get('add_to_history') == 'true':
                    # Si el usuario existe y se está agregando al historial, solo guarda el registro
                    form.save()
                    return JsonResponse({'success': True})
                else:
                    # Si el usuario existe y no se está agregando al historial, simplemente se sale
                    return JsonResponse({'documento_existente': True, 'add_to_history': False})
            except Users.DoesNotExist:
     
                if edad and edad < edad_minima:
                    form.save()
                    return JsonResponse({'menor_de_edad': True, 'success': True})
                else:
                    form.save()
                    return JsonResponse({'success': True, 'menor_de_edad': False})
        else:
            # Extraer y concatenar los mensajes de error
            errors = {field: ' '.join(error) for field, error in form.errors.items()}
            return JsonResponse({'errors': errors})
    else:
        form = UserRegistrationForm()
        return render(request, 'registro.html', {'form': form})

#----------------------------------------TABLA DE LOS USUARIOS ACTIVOS-----------------------------------------------
def usuariosActivos(request):
    return render(request, 'usuariosActivos.html', {'section': 'usuariosActivos'})

def listarUsuariosActivos(request):
    active_users = Users.objects.filter(id_state=1).values()
    data = {'users': list(active_users)}
    return JsonResponse(data)

# --------------------------------------OBTENER LOS REGISTROS DEL HISTORIAL------------------------------------------
def historial(request):
    user_id = request.GET.get('user_id')
    if not user_id:
        raise Http404("User ID not found")
    habitaciones = Bedrooms.objects.filter(deleted_at__isnull=True).values('id_bedroom', 'bedroom_name')

    context = {
        'habitaciones': habitaciones,
        'user_id': user_id,
    }

    return render(request, 'historial.html', context)

def listarRegistros(request, user_id):
    registros = Registers.objects.filter(id_user=user_id).annotate(
        bedroom_name=F('id_bedroom__bedroom_name')
    ).values('id_register', 'check_in_date', 'check_out_date', 'bedroom_name')

    data = {
        'registros': list(registros),

    }
    return JsonResponse(data)

def crear_registro(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            user_id = request.POST.get('user_id')
            if user_id:
                try:
                    user = Users.objects.get(pk=user_id)  # Obtén la instancia del usuario
                    registro.id_user = user
                    registro.save()
                    return JsonResponse({'message': 'Registro creado correctamente'}, status=200)
                except Users.DoesNotExist:
                    return JsonResponse({'message': 'User ID is invalid'}, status=400)
            else:
                return JsonResponse({'message': 'User ID is missing'}, status=400)
        else:
             # Extraer y concatenar los mensajes de error
            errors = {field: ' '.join(error) for field, error in form.errors.items()}
            return JsonResponse({'errors': errors})
    return JsonResponse({'message': 'Método no permitido'}, status=405)

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
    
def procesar_imagen(imagen):
    try:
        # Verificar el tamaño del archivo
        if imagen.size > MAX_IMAGE_SIZE_BYTES:
            raise ValueError("La imagen excede el tamaño máximo permitido")
        
        img = Image.open(imagen)

        width, height = img.size

        # Definir un tamaño máximo permitido para la imagen (en píxeles)
        max_width = 1920
        max_height = 1080

        # Verificar si la imagen excede el tamaño máximo permitido
        if width > max_width or height > max_height:
            # Redimensionar la imagen manteniendo la proporción
            img.thumbnail((max_width, max_height))

        img = img.convert('RGB') 
        
    
        output = BytesIO()
        img.save(output, format='JPEG', optimize=True, quality=85)
        output.seek(0)

        # Crear un nuevo InMemoryUploadedFile
        imagen = InMemoryUploadedFile(output, 'ImageField', imagen.name, 'image/jpeg', sys.getsizeof(output), None)

        return imagen
        
    except UnidentifiedImageError:
        raise ValueError("El archivo no es una imagen válida")
    
# def eliminar_imagen(ruta_imagen):
#     if os.path.exists(ruta_imagen):
#         os.remove(ruta_imagen)
    
@login_required
def habitaciones(request):
    habitaciones = Bedrooms.objects.filter(deleted_at__isnull=True)
    estados = States.objects.filter(id_type_state=2)
    # Obtener las imágenes de la caché o de la base de datos si no están en caché
    for habitacion in habitaciones:
        imagen_cache_key = f"imagen_{habitacion.id_bedroom}"
        imagen = cache.get(imagen_cache_key)
        if not imagen:
            # Si la imagen no está en caché, obténla de la base de datos y guárdala en caché
            imagen = habitacion.photo.read()
            cache.set(imagen_cache_key, imagen, timeout=3600)

    return render(request, 'habitaciones.html', {'habitaciones': habitaciones, 'estados': estados})

@login_required
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
        
        # Devolver el estado actualizado de la habitación
        data = {
            'id_bedroom': habitacion.id_bedroom,
            'estado': habitacion.id_state.state_name,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'La solicitud debe ser de tipo POST.'})
    
@login_required
def crear_habitacion(request):
    if request.method == 'POST':
        nombre_habitacion = request.POST.get('nombre_habitacion')
        limite_personas = request.POST.get('limite_personas')
        foto_habitacion = request.FILES.get('foto_habitacion')

        try:
            procesar_imagen(foto_habitacion)

            habitacion = Bedrooms(bedroom_name=nombre_habitacion, people_limit=limite_personas, photo=foto_habitacion)
            habitacion.save()

            return JsonResponse({'mensaje': 'Habitación creada exitosamente'})
        
        except ValueError as e:
            return JsonResponse({'error': str(e), 'excede_tamano': True}, status=400)
    

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def eliminar_imagen(habitacion_id):
    habitacion = Bedrooms.objects.get(id_bedroom=habitacion_id)

    # Obtener la ruta completa de la imagen
    ruta_imagen = os.path.join(settings.MEDIA_ROOT, habitacion.photo.name)

    # Eliminar la imagen si existe
    if os.path.exists(ruta_imagen):
        os.remove(ruta_imagen)
        print(f"La imagen {ruta_imagen} ha sido eliminada correctamente.")
    else:
        print(f"La imagen {ruta_imagen} no existe.")
    
@login_required
def eliminar_habitacion(request, habitacion_id):
    try:
        habitacion = Bedrooms.objects.get(id_bedroom=habitacion_id)
        
        habitacion.deleted_at = timezone.now()
        habitacion.save()

        eliminar_imagen(habitacion_id)

        return JsonResponse({'mensaje': 'Habitación eliminada correctamente'})
    except Bedrooms.DoesNotExist:
        return JsonResponse({'error': 'La habitación no existe'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@login_required
def detalle_habitacion(request, habitacion_id):
    habitacion = Bedrooms.objects.get(id_bedroom=habitacion_id)
    registros = Registers.objects.filter(id_bedroom=habitacion_id)
    usuarios = Users.objects.filter(id_user__in=registros.values_list('id_user', flat=True), id_state=1)

    return render(request, 'detalle_habitacion.html', {'habitacion': habitacion, 'usuarios': usuarios})

def detalle_habitacionJson(request, habitacion_id):
    habitacion = Bedrooms.objects.get(id_bedroom=habitacion_id)

    data = {
            'bedroom_name': habitacion.bedroom_name,
            'people_limit': habitacion.people_limit,
            'photo_url': habitacion.photo.url if habitacion.photo else None  # Devuelve la URL de la foto o None si no hay foto

        }
    return JsonResponse(data)

@login_required
def update_habitacion(request, habitacion_id):
    if request.method == "POST":
        try:
            habitacion = Bedrooms.objects.get(id_bedroom=habitacion_id)
        except Bedrooms.DoesNotExist:
            return JsonResponse({'error': 'Habitación no encontrada'}, status=404)

        bedroom_name = request.POST.get('nombre_habitacion')
        people_limit = request.POST.get('limite_personas')

        if bedroom_name is not None:
            habitacion.bedroom_name = bedroom_name

        if people_limit is not None:
            habitacion.people_limit = people_limit

        if 'foto_habitacion' in request.FILES:
            try:
                nueva_foto = request.FILES['foto_habitacion']
                
                nueva_foto = procesar_imagen(nueva_foto)


                habitacion.photo = nueva_foto

            except ValueError as e:
                return JsonResponse({'error': str(e), 'excede_tamano': True}, status=400)

        habitacion.save()

        data = {
            'bedroom_name': habitacion.bedroom_name,
            'photo_url': habitacion.photo.url if habitacion.photo else '',
            'people_limit': habitacion.people_limit,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return HttpResponseRedirect(reverse('inicio'))  
        else:
            username = form.cleaned_data.get('username')
            if username:
                if request.session.get('login_attempts', 0) >= 5:
                 
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
    return HttpResponseRedirect(reverse('login'))  
