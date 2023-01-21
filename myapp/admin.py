from django.contrib import admin
from .models import Solicitante, Usuario, Doctor, Doctorando
from django.contrib.auth.models import Permission

# Register your models here.
admin.site.register(Solicitante)
admin.site.register(Usuario)
admin.site.register(Permission)
admin.site.register(Doctorando)
admin.site.register(Doctor)