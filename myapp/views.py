from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import JsonResponse
from .models import Solicitante, Usuario, Doctor, Doctorando
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.http import HttpResponse

# Create your views here.
@login_required
def index(request):
    if Solicitante.objects.filter(user=request.user).exists():
        return render(request, 'respuesta.html',{
            'estado': Solicitante.objects.filter(user=request.user).get()
        })
    else:
         return render(request, 'index.html')


def iniciar_sesion(request):
    if request.method == 'GET':
            return render(request, 'iniciar_sesion.html')
    else:
        user = authenticate(request, email=request.POST['email'], password=request.POST['password'])    
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'iniciar_sesion.html', {
                'error': 'Usuario no registrado o contraseña incorrecta'
            })

def crear_solicitud(request):
    if request.method == 'GET':
        return render(request, 'crear_solicitud.html')
    else:
        f = request.POST
        
        if not Usuario.objects.filter(email=f['email']).exists():
            user = Usuario(
                nombre=f['nombre'],
                apellidos=f['apellidos'],
                email=f['email'],
                carnet=f['carnet'],
                pais=f['pais'],
                titulo=f['titulo'],
                areaTrabajo=f['area']
            )
            user.set_password(f['password'])
            user.save()
            s = Solicitante(user=user)
            s.save()
            
            
            login(request,user)
            
            return redirect('index')
        else:
            return render(request, 'crear_solicitud.html', {
                'error': 'Ya existe una solicitud con los datos ofrecidos'
            })
            
@login_required
def desconectar(request):
    logout(request)
    return redirect('index')

@login_required
@permission_required('myapp.view_usuario', raise_exception=True)
def administrar_user(request):
    if request.method == 'GET':
        return render(request, 'usuarios.html', {
            'usuarios': Usuario.objects.annotate(cuenta=Count('usuario_solicitante__estado')).annotate(cuentaD=Count('usuario_doctorando__user')).all(),
            'tabs': 'admin_user'
        })
    else:
        return render(request, 'usuarios.html', {
            'usuarios': Usuario.objects.annotate(cuenta=Count('usuario_solicitante__estado')).annotate(cuentaD=Count('usuario_doctorando__user')).filter(email__contains=request.POST['keywords']),
            'tabs': 'admin_user'
        })
    
@login_required
@permission_required('auth.view_group', raise_exception=True)
def administrar_roles(request):
    if request.method == "GET":
        return render(request, 'roles.html', {
        'roles': Group.objects.all(),
        'tabs': 'admin_roles'
        })                                                                                                                                                                                                                                                       
    else:
        if request.POST['nombre'] != None:
            if len(list(Group.objects.filter(name=request.POST['nombre']).values())) == 0:
                Group.objects.create(name=request.POST['nombre'])
                return  render(request, 'roles.html', {
                    'roles': Group.objects.all(),
                    'tabs': 'admin_roles'
                })
            else:
                return render(request, 'roles.html', {
                    'roles': Group.objects.all(),
                    'error': 'Este rol ya existe',
                    'tabs': 'admin_roles'
                })  
        else:
            return render(request, 'roles.html', {
                'roles': Group.objects.all(),
                'error': 'No se permiten roles sin nombres',
                'tabs': 'admin_roles'
            })
            
@login_required
@permission_required('auth.delete_group', raise_exception=True)
def eliminar_rol(request, nombre):
    Group.objects.filter(name=nombre).delete()
    
    return redirect('admin_roles')

@login_required
@permission_required('auth.change_group', raise_exception=True)
def permisos_roles(request, nombre):
    if request.method == 'POST':
        perm = Permission.objects.filter(name=request.POST['permiso']).get()
        g = Group.objects.filter(name=nombre).get()
        g.permissions.add(perm)
    
    permisos = list(Permission.objects.all().values('name'))
    g = Group.objects.filter(name=nombre)
    actuales = list(g.get().permissions.all().values('name'))
    
    for p in permisos:
        if p in actuales:
            permisos.remove(p)
    
    return render(request, 'permisos_roles.html', {
        'permisos': permisos,
        'grupo': actuales,
        'rol': nombre,
    })
    
@login_required
@permission_required('auth.change_group', raise_exception=True)
def eliminar_permiso_rol(request, rol, permiso):
    perm = Permission.objects.filter(name=permiso).get()
    g = Group.objects.filter(name=rol).get()
    g.permissions.remove(perm)
    
    return redirect('permisos_roles',rol)


@login_required
@permission_required('myapp.add_usuario', raise_exception=True)
def crear_usuario(request):
    if request.method == 'GET':
        return render(request, 'info_usuario.html', {
            'accion': 'crear',
            'roles': Group.objects.all()
        })
    else:
        if request.POST['password'] == "":
            return render(request, 'info_usuario.html', {
                'accion': 'crear',
                'roles': Group.objects.all(),
                'error': 'Campos obligatorios vacíos'
            })
        else:
            if not Usuario.objects.filter(email=request.POST['email']).exists() and not Usuario.objects.filter(carnet=request.POST['carnet']).exists():
                user = Usuario(
                    email = request.POST['email'],
                    nombre = request.POST['nombre'],
                    apellidos = request.POST['apellidos'],
                    carnet = request.POST['carnet'],
                    pais = request.POST['pais'],
                    titulo = request.POST['titulo'],
                    areaTrabajo = request.POST['area'],
                    sexo = request.POST['sexo'],
                    is_casado = True if len(request.POST.getlist('casado')) > 0 else False
                )
                
                user.set_password(request.POST['password'])        
                user.save()
                
                for rol in request.POST.getlist('roles'):
                    r = Group.objects.filter(name=rol).get()
                    if r is not None:
                        user.groups.add(r)
                
                return redirect('admin_user')
            else:
                return render(request, 'info_usuario.html', {
                    'accion': 'crear',
                    'roles': Group.objects.all(),
                    'error': 'El usuario ya existe'
                })
    
    
@login_required
@permission_required('myapp.change_usuario', raise_exception=True)
def editar_usuario(request, id):
    if request.method == 'GET':
        return render(request, 'info_usuario.html', {
            'accion': 'editar',
            'roles': Group.objects.all(),
            'usuario': Usuario.objects.filter(pk=id).get()
        })
    else:
        print(request.POST)
        user = Usuario.objects.filter(pk=id).get()
        user.nombre = request.POST['nombre']
        user.apellidos = request.POST['apellidos']
        user.pais = request.POST['pais']
        user.titulo = request.POST['titulo']
        user.areaTrabajo = request.POST['area']
        user.sexo = request.POST['sexo']
        user.is_casado = True if len(request.POST.getlist('casado')) > 0 else False
        
        user.groups.clear()
        
        for rol in request.POST.getlist('roles'):
            r = Group.objects.filter(name=rol).get()
            if r is not None:
                user.groups.add(r)
                
        user.save()
        
        return redirect('admin_user')
    
@login_required
@permission_required('auth.view_permission', raise_exception=True)
def view_permisos(request):
    return render(request, 'permisos.html', {
        'permisos': Permission.objects.all(),
        'tabs': 'view_permisos'
    })

@login_required
@permission_required('auth.add_permission', raise_exception=True)
def crear_permisos(request):
    if request.method == 'GET':
        return render(request, 'crear_permiso.html', {
          'tipos': ContentType.objects.all()
        })
    else:
        if not Permission.objects.filter(codename=request.POST['codename']).exists():
            ct = ContentType.objects.filter(id=request.POST['content_type']).get()
            p  = Permission(
                name = request.POST['name'],
                content_type = ct,
                codename = request.POST['codename']
            )
            p.save()
            return redirect('view_permisos') 
        else:
            return render(request, 'crear_permiso.html', {
                'tipos': ContentType.objects.all(),
                'error': 'El permiso ya existe'
            })

@login_required
@permission_required('auth.delete_permission', raise_exception=True)
def eliminar_permiso(request, codename):
    p = Permission.objects.filter(codename=codename)
    p.delete()
    return redirect('view_permisos')

@login_required 
@permission_required('myapp.evaluar_solicitud', raise_exception=True)
def view_solicitudes(request):
    if request.method == 'GET':
        return render(request, 'solicitudes.html',{
            'solicitudes': Solicitante.objects.select_related('user'),
            'tabs': 'view_solicitudes'
        })
    else:
        solicitudes = Solicitante.objects.select_related('user').filter(user__email__contains=request.POST['keywords'])
        return render(request, 'solicitudes.html',{
            'solicitudes': solicitudes,
            'tabs': 'view_solicitudes'
        })

@login_required
@permission_required('myapp.evaluar_solicitud', raise_exception=True)
def denegar_solicitud(request, id):
    user = Usuario.objects.get(pk=id)
    s = Solicitante.objects.get(user=user)
    s.estado = 'C'
    s.save()
    return redirect('view_solicitudes')

@login_required
@permission_required('myapp.evaluar_solicitud', raise_exception=True)
def aceptar_solicitud(request, id):
    user = Usuario.objects.get(pk=id)
    s = Solicitante.objects.get(user=user)
    s.delete()
    
    doctorando = Doctorando(user=user)
    doctorando.save()
    
    return redirect('view_solicitudes')


@login_required
@permission_required('myapp.view_doctor', raise_exception=True)
def view_doctor(request):
    if request.method == 'GET':
      return render(request, 'vista_doctores.html',{
        'doctores': Doctor.objects.all(),
        'tabs': 'view_doctores'
      })
    else:
        doctores = Doctor.objects.all().filter(email__contains=request.POST['keywords'])
        return render(request, 'vista_doctores.html',{
            'doctores': doctores,
            'tabs': 'view_doctor'
        })
    
@login_required
@permission_required('myapp.add_doctor', raise_exception=True)
def crear_doctor(request):
    if request.method == 'GET':
        return render(request, 'info_doctores.html', {
            'accion': 'crear'
        })
    else:
        f = request.POST
        
        if not Doctor.objects.filter(email=f['email']).exists():
            
            if len(f.getlist('casado')) > 0:
                b = True
            else:
                b = False
            
            doctor = Doctor(
                nombre = f['nombre'],
                apellidos = f['apellidos'],
                email = f['email'],
                carnet = f['carnet'],
                pais = f['pais'],
                areaPosgrado = f['area'],
                sexo = f['sexo'],
                is_casado = b,
            )
            
            doctor.save()
            
            return redirect('view_doctores')
        else:
            return render(request, 'info_doctores.html', {
                'accion': 'crear',
                'error': 'El doctor ya existe'
            })
    
@login_required
@permission_required('myapp.change_doctor', raise_exception=True)
def editar_doctor(request,id):
    if request.method == 'GET':
        return render(request, 'info_doctores.html', {
            'accion': 'editar',
            'doctor': Doctor.objects.filter(pk=id).get()
        })
    else:
        doctor = Doctor.objects.filter(pk=id).get()
        doctor.nombre = request.POST['nombre']
        doctor.apellidos = request.POST['apellidos']
        doctor.carnet = request.POST['carnet']
        doctor.pais = request.POST['pais']
        doctor.sexo = request.POST['sexo']
        doctor.email = request.POST['email']
        doctor.areaPosgrado = request.POST['area']
        doctor.is_casado = True if len(request.POST.getlist('casado')) > 0 else False
            
        doctor.save()
            
        return redirect('view_doctores')
    
@login_required
@permission_required('myapp.delete_doctor', raise_exception=True)
def eliminar_doctor(request, id):
    
    d = get_object_or_404(Doctor, pk=id)
    d.delete()
    
    return redirect('view_doctores')

@login_required
@permission_required('myapp.view_doctorando', raise_exception=True)
def view_doctorandos(request):
    if request.method == 'GET':
      return render(request, 'doctorandos.html',{
        'doctorandos': Doctorando.objects.select_related('user','tutor'),
        'tabs': 'view_doctorandos'
       })
    else:
      doctorandos = Doctorando.objects.select_related('user').filter(user__email__contains=request.POST['keywords'])
      return render(request, 'doctorandos.html',{
            'doctorandos': doctorandos,
            'tabs': 'view_doctorandos'
      })
    
@login_required
@permission_required('myapp.add_doctorando', raise_exception=True)
def nuevo_doctorando(request):
    if request.method == 'GET':
        return render(request, 'crear_doctorando.html',{
            'doctores': Doctor.objects.all()
        })
    else:
        if Usuario.objects.filter(email=request.POST['email']).exists():
            return render(request, 'crear_doctorando.html',{
                'doctores': Doctor.objects.all(),
                'error': 'El doctorando ya existe'
            })
        else:
            user = Usuario(
                email = request.POST['email'],
                nombre = request.POST['nombre'],
                apellidos = request.POST['apellidos'],
                carnet = request.POST['carnet'],
                pais = request.POST['pais'],
                titulo = request.POST['titulo'],
                areaTrabajo = request.POST['area'],
                sexo = request.POST['sexo'],
                is_casado = True if len(request.POST.getlist('casado')) > 0 else False
            )
            
            user.set_password(request.POST['password'])
            user.save()
            
            doctorando = Doctorando(
                user = user,
                tipoTesis = request.POST['tesis'],
                is_master = True if len(request.POST.getlist('master')) > 0 else False,
                tutor = Doctor.objects.get(pk=request.POST['tutor'])
            )
            
            doctorando.save()
            
            return redirect('view_doctorandos')

@login_required
@permission_required('myapp.change_doctorando', raise_exception=True)
def editar_doctorando(request, id):
    if request.method == 'GET':
        return render(request, 'editar_doctorando.html',{
            'doctores': Doctor.objects.all(),
            'doctorando': Doctorando.objects.select_related('user','tutor').get(pk=id)
        })
    else:
        d = get_object_or_404(Doctorando, pk=id)
        
        user = Usuario.objects.get(pk=d.user.id)
        user.nombre = request.POST['nombre']
        user.apellidos = request.POST['apellidos']
        user.pais = request.POST['pais']
        user.titulo = request.POST['titulo']
        user.areaTrabajo = request.POST['area']
        user.sexo = request.POST['sexo']
        user.is_casado = True if len(request.POST.getlist('casado')) > 0 else False
        user.save()
            
        d.tipoTesis = request.POST['tesis']
        d.is_master = True if len(request.POST.getlist('master')) > 0 else False
        d.tutor = Doctor.objects.get(pk=request.POST['tutor'])   
        d.save()
            
        return redirect('view_doctorandos')
            

def eliminar_usuario(request,id, ruta):
    user = get_object_or_404(Usuario, pk=id)
    
    user.delete()
    
    return redirect(ruta)

@login_required
@permission_required('myapp.delete_usuario', raise_exception=True)
def eliminar_usuario_desde_admin(request, id):
    return eliminar_usuario(request, id, 'admin_user')
    
@login_required
@permission_required('myapp.delete_doctorando', raise_exception=True)
def eliminar_doctorando(request, id):
    return eliminar_usuario(request, id, 'view_doctorandos')
        

@login_required
def cambiar_password(request):
    if request.method == 'GET':
        return render(request, 'cambiar_pass.html')
    else:
        user = request.user
        
        if request.POST['pass1'] == request.POST['pass2']:
            user.set_password(request.POST['pass1'])
            user.save()
            return redirect('index')
        else:
            return render(request, 'cambiar_pass.html', {
                'error': 'Las contraseñas no coinciden'
            })
            
@login_required
@permission_required('myapp.generar_reporte', raise_exception=True)
def generar_reporte(request):
    return render(request, 'generar_reporte.html', {
        'tabs': 'generar_reporte'
    })

@login_required
@permission_required('myapp.generar_reporte', raise_exception=True)
def generar_reporte_solicitantes(request,fechaI,fechaF):

    solicitantes = list(Solicitante.objects.filter(user__fecha_registro__gte=fechaI, user__fecha_registro__lte=fechaF).values())   

    for s in solicitantes:
        user = Usuario.objects.get(pk=s['user_id'])
        s['nombre'] = user.nombre
        s['apellidos'] = user.apellidos
        s['carnet'] = user.carnet
        s['pais'] = user.pais
        s['titulo'] = user.titulo
        s['areaTrabajo'] = user.areaTrabajo
        s['sexo'] = user.sexo
        s['is_casado'] = user.is_casado

    return JsonResponse({'solicitantes':solicitantes})



@login_required
@permission_required('myapp.generar_reporte', raise_exception=True)
def generar_reporte_doctorando(request,fechaI,fechaF,tesis):

    doctorando = list(Doctorando.objects.filter(user__fecha_registro__gte=fechaI, user__fecha_registro__lte=fechaF, tipoTesis=tesis).values())   

    for d in doctorando:
        user = Usuario.objects.get(pk=d['user_id'])
        d['nombre'] = user.nombre
        d['apellidos'] = user.apellidos
        d['carnet'] = user.carnet
        d['pais'] = user.pais
        d['titulo'] = user.titulo
        d['areaTrabajo'] = user.areaTrabajo
        d['sexo'] = user.sexo
        d['tutor'] = user.tutor
        d['is_casado'] = user.is_casado

    return JsonResponse({'doctorando':doctorando})


@login_required
@permission_required('myapp.generar_reporte', raise_exception=True)
def generar_reporte_doctor(request,fechaI,fechaF,areaPosgrado):

    if areaPosgrado == "":
        doctor = list(Doctor.objects.filter(fecha_registro__gte=fechaI, fecha_registro__lte=fechaF).values())
    else:
        doctor = list(Doctor.objects.filter(fecha_registro__gte=fechaI, fecha_registro__lte=fechaF, areaPosgrado=areaPosgrado).values())   

    for d in doctor:
        user = Usuario.objects.get(pk=d['user_id'])
        d['nombre'] = user.nombre
        d['apellidos'] = user.apellidos
        d['carnet'] = user.carnet
        d['pais'] = user.pais
        d['titulo'] = user.titulo
        d['email'] = user.email
        d['sexo'] = user.sexo
        d['is_casado'] = user.is_casado

    return JsonResponse({'doctor':doctor})



    