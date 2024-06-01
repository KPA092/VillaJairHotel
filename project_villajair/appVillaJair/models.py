from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  # Importa timezone desde django.utils

class CustomUser(User):
    class Meta:
        proxy = True

    def __str__(self):
        return self.username

User._meta.get_field('email')._unique = True


class Bedrooms(models.Model):
    id_bedroom = models.AutoField(primary_key=True)
    bedroom_name = models.CharField(max_length=40)
    people_limit = models.IntegerField()
    people_amount = models.IntegerField(null=True)
    photo = models.ImageField(upload_to="imagenes", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, default=None)
    deleted_at = models.DateTimeField(null=True, blank=True) 
    id_state = models.ForeignKey('States', models.DO_NOTHING, db_column='id_state', default=4)


    def save(self, *args, **kwargs):
        # Si se actualiza la habitación, actualiza la fecha de actualización
        if self.pk:
            self.updated_at = timezone.now()
        super(Bedrooms, self).save(*args, **kwargs)

    
    def update_room_status(self):
        # Obtener los registros activos asociados a la habitación
        active_registers = Registers.objects.filter(id_bedroom=self, id_user__id_state=1)

        # Verificar si hay algún registro activo
        if active_registers.exists():
            self.id_state_id = 3  # Estado ocupado
        else:
            self.id_state_id = 4  # Estado disponible

        # Guardar la habitación actualizada
        self.save()



class Registers(models.Model):
    id_register = models.AutoField(primary_key=True)
    check_in_date = models.DateTimeField()
    check_out_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    id_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='id_user', related_name='registers')
    id_bedroom = models.ForeignKey(Bedrooms, models.DO_NOTHING, db_column='id_bedroom')



class States(models.Model):
    id_state = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=20)
    id_type_state = models.ForeignKey('Typestates', models.DO_NOTHING, db_column='id_type_state')



class Typestates(models.Model):
    id_type_state = models.AutoField(primary_key=True)
    type_state = models.CharField(max_length=20)

    def __str__(self):
        return self.type_state


class Users(models.Model):
    id_user = models.AutoField(primary_key=True)
    document_type = models.CharField()
    nit = models.BigIntegerField()
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.BigIntegerField()
    country = models.CharField(max_length=40)
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, default=None, )
    id_state = models.ForeignKey(States, models.DO_NOTHING, db_column='id_state', blank=True, null=True)


