# Generated by Django 4.1.4 on 2023-01-09 22:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo')),
                ('nombre', models.TextField(verbose_name='Nombre')),
                ('apellidos', models.TextField(verbose_name='Apellidos')),
                ('carnet', models.CharField(max_length=11)),
                ('pais', models.TextField(null=True)),
                ('titulo', models.TextField(null=True)),
                ('areaTrabajo', models.TextField(null=True)),
                ('sexo', models.CharField(choices=[('M', 'masculino'), ('F', 'Femenino'), ('E', 'Especificar')], default='E', max_length=1)),
                ('is_casado', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('fecha_registro', models.DateField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(verbose_name='Nombre')),
                ('apellidos', models.TextField(verbose_name='Apellidos')),
                ('email', models.EmailField(max_length=254, null=True)),
                ('carnet', models.CharField(max_length=11)),
                ('pais', models.TextField(null=True)),
                ('sexo', models.CharField(choices=[('M', 'masculino'), ('F', 'Femenino'), ('E', 'Especificar')], default='E', max_length=1)),
                ('is_casado', models.BooleanField(default=False)),
                ('areaPosgrado', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Solicitante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('P', 'Pendiente'), ('C', 'Cancelada')], default='P', max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario_solicitante', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Doctorando',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipoTesis', models.TextField(null=True)),
                ('is_master', models.BooleanField(default=False)),
                ('tutor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='doctor_doctorando', to='myapp.doctor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario_doctorando', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
