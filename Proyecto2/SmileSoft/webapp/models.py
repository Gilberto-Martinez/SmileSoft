from email import message
from telnetlib import AUTHENTICATION
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, 
    BaseUserManager, 
    PermissionsMixin,)
from gestion_administrativo import *
from gestion_administrativo.models import *
from agregar_mas.models import *
from webapp import *


# Create your models here.

class ManejadorUsuario(BaseUserManager):

    # Crea y guarda a un usuario con el usuario y contraseña ingresada
    def create_user(self, usuario, password):
        if not usuario:
            raise ValueError('Debe ingresar un usuario')
        usuario_nuevo = self.model(usuario = usuario)
        usuario_nuevo.set_password(password)
        usuario_nuevo.save(using=self._db)
        return usuario_nuevo

    def create_user(self, password, numero_documento):
        if not password:
            raise ValueError('Debe ingresar una contraseña')
        if not numero_documento:
            raise ValueError('Debe ingresar un numero de documento')
        persona = Persona.objects.get(numero_documento=numero_documento)
        nombre = persona.nombre
        nombre = nombre.strip()
        apellido = persona.apellido
        apellido = apellido.strip()
        inicial = nombre[0:1].lower()
        apellido = apellido.lower()
        posicion = apellido.find(" ") # Busca un espacio en el apellido (entre el primer y segundo apellido), retorna -1 si no encuentra espacios
        if posicion != -1: # Si el apellido tiene un espacio
            apellido = apellido[0:posicion]
        nombre_usuario = inicial+apellido
        try:
            usuario_buscado = Usuario.objects.get(usuario=nombre_usuario) # Obtiene de la base de datos si ya existe el usuario
        except Usuario.DoesNotExist:# Si el usuario no existe no realiza ninguna acción
            pass
        else: # Si el usuario existe entra a un bucle while
            existe = True
            contador = 1
            nombre_usu_original = nombre_usuario
            while existe is True:# Mientras el usuario ya exista
                nombre_usuario = nombre_usu_original+str(contador) # le contatena un numero
                try:
                    usuario_buscado = Usuario.objects.get(usuario=nombre_usuario) # Busca en la base de datos el nuevo nombre de usuario contatenado
                except Usuario.DoesNotExist:# Si el usuario buscado no existe entonces mantiene el ultimo nombre de usuario generado
                    nombre_usuario = nombre_usuario
                    existe = False
                else:
                    contador = contador + 1
        usuario_nuevo = self.model(usuario = str(nombre_usuario))
        usuario_nuevo.usuario = nombre_usuario
        usuario_nuevo.numero_documento = persona
        usuario_nuevo.set_password(password)
        usuario_nuevo.save(using=self._db)
        print('*---------------------------------*')
        print('Usuario: ', nombre_usuario)
        print('Contraseña: ',password)
        return usuario_nuevo

    def cambiar_password(self, password, numero_documento):
        if not password:
            raise ValueError('Debe ingresar una contraseña')
        if not numero_documento:
            raise ValueError('Debe ingresar un numero de documento')
        usuario = Usuario.objects.get(numero_documento=numero_documento)
        nombre_usuario = usuario.usuario
        print('*---------------------------------*')
        print('Usuario: ', nombre_usuario)
        print('Contraseña: ',password)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    # Crea y guarda a un super-usuario
    def create_superuser(self, usuario, password):
        usuario_nuevo = self.create_user(usuario, password)
        usuario_nuevo.staff = True
        usuario_nuevo.superuser = True
        usuario_nuevo.is_admin = True
        usuario_nuevo.save(using=self._db)
        return usuario_nuevo


class Usuario(AbstractBaseUser, PermissionsMixin,):
    usuario = models.CharField(primary_key=True, max_length=15, help_text=(' ✏️ Ejemplo jperez'))
    numero_documento = models.OneToOneField(
                                            Persona, 
                                            blank = False, 
                                            null = False, 
                                           # verbose_name = 'Numero de documento', 
                                            on_delete = models.CASCADE, 
                                            # default = 0,
                                            unique=True
                                        ) 
 
    is_active = models.BooleanField(default=True, verbose_name='Es Activo',)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False, verbose_name='Es Administrador')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    #mensaje= models.CharField(max_length=20)
    USERNAME_FIELD = "usuario"
    objects = ManejadorUsuario()
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = ('usuario')
        #para ordenar alfabeticamente de a -z es ordering=[usuario], y si es de z -a es ordering=[-usuario]
        ordering = ['usuario']
        
    def get_full_name(self):
        return self.usuario

    def get_short_name(self):
        return self.usuario

    '''def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True'''

    # def __str__(self):
    #     return self.usuario
    
    def __str__(self):
        if self.usuario:
            # Si no está vacío, devuelve el nombre de usuario
            return self.usuario
        else:
            # Si el nombre de usuario está vacío, devuelve un objeto que no puede estar vacío
            return message("Este usuario esta vacio")


