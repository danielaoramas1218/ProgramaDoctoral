from django import template
from django.contrib.auth.models import Permission, Group
from myapp.models import Doctorando, Doctor

register = template.Library()

@register.filter(name='has_perm')
def has_perm(user, permission): 
    return user.has_perm(permission)

@register.filter(name='is_doctorando')
def is_doctorando(user): 
    return Doctorando.objects.filter(user=user).exists()

@register.filter(name='getTutor')
def getTutor(user): 
    tutor = Doctorando.objects.filter(user=user).get().tutor
    if tutor != None:
        object = Doctor.objects.filter(pk=tutor.id).get()
    else:
        object = None
    return object.nombre + " " + object.apellidos + " (" + object.email + ")" if object != None else 'Sin asignar'

@register.filter(name='getTipoTesis')
def getTipoTesis(user): 
    object = Doctorando.objects.filter(user=user).get()
    return object.tipoTesis if object.tipoTesis != None else 'Por definir'

@register.filter(name='isMaster')
def isMaster(user): 
    object = Doctorando.objects.filter(user=user).get()
    return  'Si' if object.is_master else 'No'