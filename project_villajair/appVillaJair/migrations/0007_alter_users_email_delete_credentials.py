# Generated by Django 5.0.4 on 2024-05-09 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appVillaJair', '0006_alter_registers_check_in_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.CharField(unique=True),
        ),
        migrations.DeleteModel(
            name='Credentials',
        ),
    ]
