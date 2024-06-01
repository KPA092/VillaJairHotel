import threading
import logging
import time
from django.utils import timezone
from .models import Users, Registers, States, Bedrooms

logger = logging.getLogger(__name__)

def actualizar_estado_usuarios():
    while True:
        try:
            logger.info("Tarea de actualización de estado de usuarios en ejecución...")
            usuarios = Users.objects.all()
            fecha_actual = timezone.now()

            for usuario in usuarios:
                registros_usuario = Registers.objects.filter(id_user=usuario).order_by('-created_at')
                if registros_usuario:
                    ultimo_registro = registros_usuario.first()
                    if ultimo_registro.check_in_date <= fecha_actual <= ultimo_registro.check_out_date and usuario.id_state != 1:
                        usuario.id_state = States.objects.get(id_state=1)
                        usuario.save()
                    elif fecha_actual > ultimo_registro.check_out_date or fecha_actual < ultimo_registro.check_in_date and usuario.id_state != 2:
                        usuario.id_state = States.objects.get(id_state=2)
                        usuario.save()

            logger.info("Tarea de actualización de estado de usuarios completada.")
        except Exception as e:
            logger.error(f"Error en la tarea de actualización de estado de usuarios: {e}")

        time.sleep(60)

def actualizar_estado_habitaciones():
    while True:
        try:
           # Obtener todas las habitaciones
            habitaciones = Bedrooms.objects.all()

            # Obtener todos los registros que tienen usuarios activos
            registros_con_usuarios_activos = Registers.objects.filter(id_user__id_state=1)

            # Crear un diccionario para mapear las habitaciones con registros de usuarios activos
            habitaciones_con_usuarios_activos = {registro.id_bedroom.id_bedroom for registro in registros_con_usuarios_activos}

            for habitacion in habitaciones:
                # Verificar si la habitación está en estado de mantenimiento
                if habitacion.id_state_id == 5:
                    continue  # Omitir la actualización de la habitación en mantenimiento

                if habitacion.id_bedroom in habitaciones_con_usuarios_activos:
                    habitacion.id_state = States.objects.get(id_state=3)  # Habitación ocupada
                else:
                    habitacion.id_state = States.objects.get(id_state=4)  # Habitación disponible

                habitacion.save()  # Guardar los cambios en la base de datos
        except Exception as e:
            logger.error(f"Error en la tarea de actualización de estado de usuarios: {e}")

        time.sleep(60)

def iniciar_tarea_actualizacion_habitaciones():
    actualizar_tarea = threading.Thread(target=actualizar_estado_habitaciones)
    actualizar_tarea.daemon = True
    actualizar_tarea.start()


def iniciar_tarea_actualizacion():
    actualizar_tarea = threading.Thread(target=actualizar_estado_usuarios)
    actualizar_tarea.daemon = True
    actualizar_tarea.start()


