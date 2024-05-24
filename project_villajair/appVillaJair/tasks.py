# tasks.py

import threading
import time
import logging
from django.utils import timezone
from .models import Registers, Users, States

logger = logging.getLogger(__name__)

def actualizar_estado_usuarios():
    while True:
        logger.info("Tarea de actualización de estado de usuarios en ejecución...")
        usuarios = Users.objects.all()
        fecha_actual = timezone.now().date()

        for usuario in usuarios:
            ultimo_registro = Registers.objects.filter(id_user=usuario).order_by('-check_in_date').first()
            if ultimo_registro:
                if ultimo_registro.check_in_date.date() <= fecha_actual <= ultimo_registro.check_out_date.date() and usuario.id_state_id != 1:
                    usuario.id_state = States.objects.get(id_state=1)  
                    usuario.save()
                elif fecha_actual > ultimo_registro.check_out_date.date() and usuario.id_state_id != 2:
                    usuario.id_state = States.objects.get(id_state=2) 
                    usuario.save()

        logger.info("Tarea de actualización de estado de usuarios completada.")
        time.sleep(60)  

def iniciar_tarea_actualizacion():
    actualizar_tarea = threading.Thread(target=actualizar_estado_usuarios)
    actualizar_tarea.daemon = True  
    actualizar_tarea.start()
