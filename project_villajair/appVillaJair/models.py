from django.db import models

class Bedrooms(models.Model):
    id_bedroom = models.AutoField(primary_key=True)
    bedroom_name = models.CharField(max_length=40)
    people_limit = models.IntegerField()
    people_amount = models.IntegerField()
    photo = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, default=None)
    id_state = models.ForeignKey('States', models.DO_NOTHING, db_column='id_state')


class Registers(models.Model):
    id_register = models.AutoField(primary_key=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
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

   
class Users(models.Model):
    id_user = models.AutoField(primary_key=True)
    nit = models.BigIntegerField(unique=True)
    full_name = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    phone_number = models.BigIntegerField()
    country = models.CharField(max_length=40)
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, default=None, )
    id_state = models.ForeignKey(States, models.DO_NOTHING, db_column='id_state', blank=True, null=True)
    id_bedroom = models.ForeignKey(Bedrooms, models.DO_NOTHING, db_column='id_bedroom', blank=True, null=True)
    id_role = models.ForeignKey(Role, models.DO_NOTHING, db_column='id_role')

class Credentials(models.Model):
    id_credential = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)


