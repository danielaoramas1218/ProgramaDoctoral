from django.test import TestCase,Client
import myapp.models as models
from .views import *
from django.db.utils import IntegrityError
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

class prueba(TestCase):
    def setUP(self):
         user = models.Usuario(nombre = "Daniela", apellidos = "oramas", email = "lala@gb.net" , sexo = "femenino", carnet = 99080117000,pais = "holanda", is_casado=True, areaTrabajo = "facultad 4", titulo="ingeniero",  fecha_registro="2002-2-2")
         doctor = models.Doctorando(nombre = "Daniela", apellidos = "oramas", email = "lala@gb.net" , sexo = "femenino", carnet = 99080117000,pais = "holanda", is_casado=True, areaPosgrado="mamifero",  fecha_registro="2002-2-2" )
         doctorando = models.Doctorando(user = user, tutor = doctor, tipoTesis= "ciclo", is_master="true", fecha_registro="2002-2-2")
         doctorando.save()
         doctorando = models.Doctorando(user = user, tutor = doctor, tipoTesis= "ciclocompleto", is_master="true", fecha_registro="2002-2-2" )
         doctorando.save()
         doctorando = models.Doctorando(user = user, tutor = doctor, tipoTesis= "ciclo", is_master="true", fecha_registro="2002-2-2" )
         doctorando.save()

         doctor = models.Doctor(nombre = "Daniela", apellidos = "oramas", email = "lala@gb.net" , sexo = "femenino", carnet = 99080117000,pais = "holanda", is_casado=True, areaPosgrado="mamifero",  fecha_registro="2002-2-2" )
         doctor.save()
         doctor = models.Doctor(nombre = "uasdasa", apellidos = "oramas", email = "lala@gb.net" , sexo = "masculino", carnet = 99453217000,pais = "holanda", is_casado=True, areaPosgrado="mamifero",  fecha_registro="2002-2-2" )
         doctor.save()
         doctor = models.Doctor(nombre = "asdasd", apellidos = "oramas", email = "lala@gb.net" , sexo = "femenino", carnet = 95673117000,pais = "holanda", is_casado=True, areaPosgrado="mamifero",  fecha_registro="2002-2-2" )
         doctor.save()
         pass

    def  tearDown(self) -> None:
         return super().tearDown()
         pass
    def tests_listardoctor(self):
        aux = models.Doctor.objects.all()

        self.assertIsNotNone(aux)

    def tests_RegistrarDoctor(self):

            var = True
            doctor = models.Doctor(nombre = "Daniela", apellidos = "oramas", email = "lala@gb.net" , sexo = "femenino", carnet = 99080117000,pais = "holanda", is_casado=True, areaPosgrado="mamifero",  fecha_registro="2002-2-2" )
           
            try:
              doctor.save()
            except:  
              var = False  
           
            self.assertTrue(var)
            
    def tests_modificarDoctor(self):
         doc = models.Doctor(nombre = "Daniela", apellidos = "oramas", email = "lala@gb.net" , sexo = "femenino", carnet = 99080117000,pais = "holanda", is_casado=True, areaPosgrado="mamifero",  fecha_registro="2002-2-2" )
         doc.nombre = 'aaaaaa'
         doc.apellidos = 'qwqwqw'
         doc.email ='asdasdasdasd'
         doc.sexo = 'femenino'
         doc.carnet = 99080117012
         doc.pais = 'asdasdadas'
         doc.is_casado = True
         doc.areaPosgrado = "asdasd"
         doc.fecha_registro = '2002-2-2'
         var = False
         try:
          doc.save()
          
         except:
            var = True
         self.assertFalse(var)

    def tests_eliminarDoctor(self):
         doc = models.Doctor.objects.all()
         doc.delete() 
         self.assertIsNotNone(doc)

    
    def tests_listardoctorando(self):
        aux = models.Doctorando.objects.all()

        self.assertIsNotNone(aux)

    def tests_RegistrarDoctorando(self):
            user = models.Usuario(email = "lala@gb.net", nombre = "Daniela", apellidos = "oramas", carnet = 99080117000, pais = "holanda", titulo="ingeniero", areaTrabajo = "facultad 4", sexo = "femenino", is_casado=True,  is_active=True, is_staff=True, fecha_registro="2002-2-2")
            doctor = models.Doctor(nombre = "Daniela", apellidos = "oramas", email = "lala@gb.net" , sexo = "femenino", carnet = 99080117000,pais = "holanda", is_casado=True, areaPosgrado="mamifero",  fecha_registro="2002-2-2" )
            user.save()
            doctor.save()
            var = True
            doctorando = models.Doctorando(user = user, tutor = doctor, tipoTesis= "ciclocompleto", is_master=True, fecha_registro = "2020-2-1" )
           
            try:
              doctorando.save()
            except:  
              var = False  
           
            self.assertTrue(var)
            
    def tests_modificarDoctorando(self):
         user = models.Usuario(email = "dani@gmail.com", nombre = "Daniela", apellidos = "oramas", carnet = 99080117000, pais = "holanda", titulo="ingeniero", areaTrabajo = "facultad 4", sexo = "femenino", is_casado=True,  is_active=True, is_staff=True, fecha_registro="2002-2-2")
         doctor = models.Doctor(nombre = "Daniela", apellidos = "oramas", email = "dani@gmail.com" , sexo = "femenino", carnet = 99080117000,pais = "holanda", is_casado=True, areaPosgrado="mamifero",  fecha_registro="2002-2-2" )
         user.save()
         doctor.save()
        
         doc = models.Doctorando(user = user, tutor = doctor, tipoTesis="ciclo", is_master=True,fecha_registro = "2020-2-1")
         doc.user = user
         doc.tutor = doctor
         doc.tipoTesis = "ciclo"
         doc.is_master = True
         doc.fecha_registro = "2020-2-1"
         var = False
         try:
          doc.save()
          
         except:
            var = True
         self.assertFalse(var)

    def tests_eliminarDoctorando(self):
         doc = models.Doctorando.objects.all()
         doc.delete() 
         self.assertIsNotNone(doc)

    def tests_listarUsuario(self):
        aux = models.Usuario.objects.all()

        self.assertIsNotNone(aux)

    def tests_RegistrarUsuario(self):
            user = models.Usuario(email = "dani@gmail.com", nombre = "Daniela", apellidos = "oramas", carnet = 99080117000, pais = "holanda", titulo="ingeniero", areaTrabajo = "facultad 4", sexo = "femenino", is_casado=True,  is_active=True, is_staff=True, fecha_registro="2002-2-2")

            user.save()
            var = True
           
            try:
              user.save()
            except:  
              var = False  
           
            self.assertTrue(var)
            
    def tests_modificarUsuario(self):
         user = models.Usuario(email = "dani@gmail", nombre = "daniela", apellidos = "perez", carnet = 99080117000, pais = "holanda", titulo="ingeniero", areaTrabajo = "facultad 4", sexo = "femenino", is_casado=True,  is_active=True, is_staff=True, fecha_registro="2002-2-2")
         user.email="dani@gmail"
         user.nombre="daniela"
         user.apellidos="perez"
         user.carnet=99080117000
         user.pais="holanda"
         user.titulo="ingeniero"
         user.areaTrabajo = "facultad 4" 
         user.sexo = "femenino" 
         user.is_casado=True  
         user.is_active=True 
         user.is_staff=True
         user.fecha_registro="2002-2-2"
         var=False
         try:
          user.save()
          
         except:
            var = True
         self.assertFalse(var)

    def tests_eliminarUsuario(self):
         user = models.Usuario.objects.all()
         user.delete() 
         self.assertIsNotNone(user) 

    def tests_listardoctor(self):
        aux = models.Doctor.objects.all()

        self.assertIsNotNone(aux)

    def tests_RegistrarSolicitante(self):

            user = models.Usuario(email = "dani@gmail.com", nombre = "Daniela", apellidos = "oramas", carnet = 99080117000, pais = "holanda", titulo="ingeniero", areaTrabajo = "facultad 4", sexo = "femenino", is_casado=True,  is_active=True, is_staff=True, fecha_registro="2002-2-2")
           
            user.save()
            
            var = True
            solicitante = models.Solicitante(user = user, estado = "P" )
           
            try:
              solicitante.save()
            except:  
              var = False  
           
            self.assertTrue(var)
            
    def tests_modificarSolicitante(self):
            user = models.Usuario(email = "lala@gb.net", nombre = "Daniela", apellidos = "oramas", carnet = 99080117000, pais = "holanda", titulo="ingeniero", areaTrabajo = "facultad 4", sexo = "femenino", is_casado=True,  is_active=True, is_staff=True, fecha_registro="2002-2-2")
            user.save()
            
            var = True
            solicitante = models.Solicitante(user = user, estado= "P" )
           
            try:
             solicitante.save()
            except:  
              var = False  
           
            self.assertTrue(var)
    def tests_eliminarSolicitante(self):
         Solicitante = models.Solicitante.objects.all()
         Solicitante.delete() 
         self.assertIsNotNone(Solicitante)
       
class UsuarioTestCase(TestCase):
    #Creando los usuarios para empezar las pruebas
    def setUp(self):
        self.superuser = get_user_model().objects.create_superuser(
                                            email = "yani@gb.net", 
                                            nombre = "yanitza", 
                                            apellidos = "help",
                                            carnet = 99080117000,
                                            pais = "holanda",
                                            titulo="ingeniero",
                                            areaTrabajo = "facultad 4",
                                            
                                          
                                          
                                            password = '12345678'
                                            )
        self.cliente = get_user_model().objects.create_user(
                                            email = "dani@gb.net", 
                                            nombre = "dani", 
                                            apellidos = "hi",
                                            carnet = 99080117001,
                                            pais = "cuba",
                                            titulo="ingeniero",
                                            areaTrabajo = "facultad 1",
                                            password = '12345678'
                                            )                                    
        self.user = models.Usuario()
        self.user.nombre = "Daniela"
        self.user.apellidos = "oramas" 
        self.user.email = "lala@gb.net"
        self.user.sexo = "femenino" 
        self.user.carnet = 99080117003
        self.user.pais = "holanda" 
        self.user.is_casado=True
        self.user.areaTrabajo = "facultad 4"
        self.user.titulo="ingeniero"
        self.user.fecha_registro="2002-2-2"
        self.user.password = '12345678'
        self.user.save()
        pass
    def test_User_create(self):
        # Los Usuarios son creados correctamente
        self.assertEqual(self.superuser.nombre,'yanitza')
        self.assertEqual(self.cliente.nombre,'dani')

       
    def test_User_edit(self):
        # Los Usuarios son editados correctamente correctamente
        user =  models.Usuario.objects.get(email="yani@gb.net")
        user.email = 'clienteedit@uci.cu'
        user.save()
        self.assertEqual(user.email, 'clienteedit@uci.cu')
    
    def test_login(self):
        #el ususrio se logea correctamente
        self.client.login(username='yani@gb.net', password='12345678')
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        
    def test_create_User_with_empty_fields(self):
        with self.assertRaises(IntegrityError):
           user = models.Usuario.objects.create_user(
                                            email = None, 
                                            nombre = None, 
                                            apellidos = None,
                                            carnet = None,
                                            pais = None,
                                            titulo=None,
                                            areaTrabajo = None,
                                            password = None
                                            )  

    def test_get_User_non_existing(self):
        with self.assertRaises(models.Usuario.DoesNotExist):
            models.Usuario.objects.get(pk="20")

class DoctorTestCase(TestCase):
    def setUp(self):
        self.superuser = get_user_model().objects.create_superuser(
                                            email = "yani@gb.net", 
                                            nombre = "yanitza", 
                                            apellidos = "help",
                                            carnet = 99080117000,
                                            pais = "holanda",
                                            titulo="ingeniero",
                                            areaTrabajo = "facultad 4",
                                            password = '12345678'
                                            )
        self.cliente = get_user_model().objects.create_user(
                                            email = "dani@gb.net", 
                                            nombre = "dani", 
                                            apellidos = "hi",
                                            carnet = 99080117001,
                                            pais = "cuba",
                                            titulo="ingeniero",
                                            areaTrabajo = "facultad 1",
                                            password = '12345678'
                                            )
        self.user = models.Doctor()
        self.user.nombre = "Daniela"
        self.user.apellidos = "oramas" 
        self.user.email = "lala@gb.net"
        self.user.sexo = "femenino" 
        self.user.carnet = 99080117003
        self.user.is_casado=True
        self.user.areaTrabajo = "facultad 4"
        self.user.save()
        pass
    def test_Doctor_create(self):
        # Los Usuarios son creados correctamente
        self.client.login(username='yani@gb.net', password='12345678')
        response = self.client.post(reverse('crear_doctores'), {'nombre':'Doctor','apellidos': 'Juan', 'email':'juan@uci.cu', 'carnet': 99061418171,'pais':'cuba','sexo':'M','is_casado':True,'area':'facultad 1'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/doctores/'))
        Created = models.Doctor.objects.get(nombre="Doctor")
        self.assertIsInstance(Created,models.Doctor)
        self.assertEqual(Created.nombre, 'Doctor')
    
    def test_Doctor_edit(self):
        # Los Usuarios son creados correctamente
        self.client.login(username='yani@gb.net', password='12345678')
        response = self.client.post(reverse('crear_doctores'), {'nombre':'Doctor','apellidos': 'Juan', 'email':'juan@uci.cu', 'carnet': 99061418171,'pais':'cuba','sexo':'M','is_casado':True,'area':'facultad 1'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/doctores/'))
        Created = models.Doctor.objects.get(nombre="Doctor")
        self.assertIsInstance(Created,models.Doctor)
        self.assertEqual(Created.nombre, 'Doctor')
        Doctor = models.Doctor.objects.get(nombre="Doctor")
        Doctor.nombre='editado'
        Doctor.save()
        self.assertEqual(Doctor.nombre, 'editado')

    def test_create_Doctor_with_empty_fields(self):
        with self.assertRaises(IntegrityError):
           user = models.Doctor.objects.create(
                                            email = None, 
                                            nombre = None, 
                                            apellidos = None,
                                            carnet = None,
                                            pais = None,
                                            )  

    def test_get_Doctor_non_existing(self):
        with self.assertRaises(models.Doctor.DoesNotExist):
            models.Doctor.objects.get(pk="20")

class DoctorandoTestCase(TestCase):
    def setUp(self):
        self.superuser = get_user_model().objects.create_superuser(
                                            email = "yani@gb.net", 
                                            nombre = "yanitza", 
                                            apellidos = "help",
                                            carnet = 99080117000,
                                            pais = "holanda",
                                            titulo="ingeniero",
                                            areaTrabajo = "facultad 4",
                                            
                                          
                                          
                                            password = '12345678'
                                            )
        self.cliente = get_user_model().objects.create_user(
                                            email = "dani@gb.net", 
                                            nombre = "dani", 
                                            apellidos = "hi",
                                            carnet = 99080117001,
                                            pais = "cuba",
                                            titulo="ingeniero",
                                            areaTrabajo = "facultad 1",
                                            password = '12345678'
                                            )                                    
        self.user = models.Usuario()
        self.user.nombre = "Daniela"
        self.user.apellidos = "oramas" 
        self.user.email = "lala@gb.net"
        self.user.sexo = "femenino" 
        self.user.carnet = 99080117003
        self.user.pais = "holanda" 
        self.user.is_casado=True
        self.user.areaTrabajo = "facultad 4"
        self.user.titulo="ingeniero"
        self.user.fecha_registro="2002-2-2"
        self.user.password = '12345678'
        self.user.save()

        self.doctor =models.Doctor()
        self.doctor.nombre = "Doctor"
        self.doctor.apellidos = "oramas" 
        self.doctor.email = "lala@gb.net"
        self.doctor.sexo = "femenino" 
        self.doctor.carnet = 99080117003
        self.doctor.is_casado=True
        self.doctor.areaTrabajo = "facultad 4"
        self.doctor.save()
        pass
    def test_doctorando_created(self):
        self.assertEqual(self.user.nombre,'Daniela')
        self.assertEqual(self.doctor.nombre,'Doctor')
        doctorando = models.Doctorando()
        doctorando.user=self.user
        doctorando.tutor=self.doctor
        doctorando.tipoTesis='Tesis'
        doctorando.is_master = True
        doctorando.save
        self.assertIsInstance(doctorando,models.Doctorando)
        self.assertEqual(doctorando.user.nombre,'Daniela')

    def test_doctorando_edit(self):
        doctorando = models.Doctorando()
        doctorando.user=self.user
        doctorando.tutor=self.doctor
        doctorando.tipoTesis='Tesis'
        doctorando.is_master = True
        doctorando.save()
        self.assertIsInstance(doctorando,models.Doctorando)
        self.assertEqual(doctorando.user.nombre,'Daniela')
        doctorando.tipoTesis='No se hizo'
        doctorando.save()
        self.assertEqual(doctorando.tipoTesis,'No se hizo')

    def test_grupos(self):
        self.client.login(username='yani@gb.net', password='12345678')
        response = self.client.post(reverse('admin_roles'), {'nombre':'Doctor'})
        self.assertEqual(response.status_code, 200)
        Created = Group.objects.get(name="Doctor")
        self.assertIsInstance(Created,Group)
        self.assertEqual(Created.name, 'Doctor')
