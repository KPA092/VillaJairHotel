import threading
import logging
import time
from django.utils import timezone
from .models import Users, Registers, States

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

def iniciar_tarea_actualizacion():
    actualizar_tarea = threading.Thread(target=actualizar_estado_usuarios)
    actualizar_tarea.daemon = True
    actualizar_tarea.start()
