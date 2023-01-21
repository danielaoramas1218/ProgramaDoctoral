# Generated by Django 4.1.4 on 2023-01-12 06:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_doctor_fecha_registro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='email',
            field=models.EmailField(max_length=254, unique=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$', 'Correo Invalido')], verbose_name='Correo'),
        ),
    ]