from django.db import models
from django.contrib.auth.models import User

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
    people_amount = models.IntegerField()
    photo = models.ImageField(upload_to="imagenes", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, default=None)
    id_state = models.ForeignKey('States', models.DO_NOTHING, db_column='id_state')



class Registers(models.Model):
    id_register = models.AutoField(primary_key=True)
    check_in_date = models.DateTimeField()
    check_out_date = models.DateTimeField()
    id_user = models.ForeignKey('Users', models.DO_NOTHING, db_column='id_user')
    id_bedroom = models.ForeignKey(Bedrooms, models.DO_NOTHING, db_column='id_bedroom')



class Role(models.Model):
    id_role = models.AutoField(primary_key=True)
    role = models.CharField(max_length=20)




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
    nit = models.BigIntegerField(unique=True)
    full_name = models.CharField(max_length=150)
    email = models.CharField(unique=True)
    phone_number = models.BigIntegerField()
    country = models.CharField(max_length=40)
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, default=None, )
    id_state = models.ForeignKey(States, models.DO_NOTHING, db_column='id_state', blank=True, null=True)
    id_bedroom = models.ForeignKey(Bedrooms, models.DO_NOTHING, db_column='id_bedroom', blank=True, null=True)
    id_role = models.ForeignKey(Role, models.DO_NOTHING, db_column='id_role')
