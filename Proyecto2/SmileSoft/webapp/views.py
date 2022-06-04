from http.client import HTTPResponse
from msilib.schema import Class
from multiprocessing import context
from pickle import FALSE, TRUE
import re
from ssl import ALERT_DESCRIPTION_CERTIFICATE_UNOBTAINABLE
from tkinter.tix import Form
from winreg import QueryValue
from xml.dom import UserDataHandler
from django import dispatch
from django.conf import settings
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, get_list_or_404
from django.http import HttpResponseRedirect, JsonResponse, request
from django.urls import reverse_lazy
from webapp.forms import *
from .forms import *
from django.contrib import messages
from django.http import (
    Http404, HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect,)
from django.views.generic.list import ListView
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db.models import Q

# Estos import son para modificar contraseña
from django.views.generic import FormView, TemplateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from logging import PlaceHolder, raiseExceptions
from multiprocessing import context
from turtle import title
from django.views.generic import View
from webapp.models import Usuario
from django.contrib.auth.models import auth
from django.contrib.auth import login, logout, authenticate
from .mixins import LoginMixin
from django.contrib.auth.views import LoginView, PasswordResetView
# from webapp.forms import ResetPasswordForm
from .forms import UsuarioLoginForm, PersonaInvitadaForm
from django.template.loader import render_to_string
import SmileSoft.settings as setting

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import PermissionDenied
from django.http import Http404

from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.generic import CreateView
from django.contrib.auth.models import Group
from gestion_administrativo.forms import PacienteForm, PersonaForm
from gestion_administrativo.models import Paciente, Persona
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect

'''Inicio de Sesion'''
#------------------------------------------------------------------------------------------------------#
# Vista de Login


def inicio_login(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['usuario'],
            password=request.POST['password1']
        )
        if user is not None:
            login(request, user)
            print("Autentica.....................................")
            messages.info(
                request, f" ✔ Usted {user.usuario} ha iniciado sesión correctamente ")
            return redirect("/panel_control/inicio/")
        else:
            # messages.info(request, f'Usuario Invalido')
            messages.error(
                request, f"✘ El usuario o la contraseña es incorrecto")

            print("AQUI ENTRA cuando es vacio o NO VALIDO")
    return render(request, "inicio/login.html")

# Vista de Cerrar sesión

def cerrar_sesion(request):
    logout(request)
    messages.info(
        request, f"✔ Tu sesión se ha cerrado correctamente")
    return redirect("/login/")

# def inicio_prueba(request):

#     return render(request, "inicio/inicio_prueba.html")


# def prueba(request):

#     return render(request, "prueba.html")

#----------------------------------------------------PACIENTE--------------------------------------------------#

#------------------------------------------------------------------------------------------------------#
# Formulario de Registro de Paciente
class MensajeView(TemplateView):
    template_name= 'inicio/mensaje_redireccion.html'

class UsuarioConfirmacionView(TemplateView):
    template_name= "inicio/confirmacion_usuario.html"


def mostrar_mensaje_confirmacion(self,): #cedula):
    return render(request, "inicio/mensaje_confirmacion.html",)# cedula)


def consultar_cedula(request):
    data = {
            'form': ConsultaInvitadoForm()
    }
    if request.method == 'POST':
        form = ConsultaInvitadoForm(data=request.POST)
        if form.is_valid():
            invitado = form.save(commit=False)
            cedula = invitado.numero_documento
            try: # Verificar si esta registrado como paciente 
                paciente = Paciente.objects.get(numero_documento=cedula)
            except ObjectDoesNotExist:# Si no se encuentra registrado como paciente
                return redirect("/mensaje/")
            else:#Si se encuentra registrado como paciente
                try: # Verificar si cuenta con un usuario
                    usuario = Usuario.objects.get(numero_documento=cedula)
                except ObjectDoesNotExist:# Si no cuenta con un usuario
                    # return redirect("/mensaje_confirmacion/%s" %(cedula))
                    return redirect("/mensaje_confirmacion/")
                else:# Si ya cuenta con un usuario
                    return redirect("/confirmacion_usuario/")

    return render(request, "inicio/consultar_documento.html", data)

def generar_usuario_paciente(self, cedula):
    persona = Persona.objects.get(numero_documento=cedula)
    nombre = persona.nombre
    apellido = persona.apellido
    inicial = nombre[0:1].lower()
    apellido = apellido.lower()
    nombre_usuario = inicial+apellido
    password = User.objects.make_random_password()
    usuario = Usuario.objects.create_user(nombre_usuario, password, cedula)
    email = persona.correo_electronico


# class FormInvitadoCreate(CreateView):
#     model = Persona
#     template_name = 'inicio/registro_invitado.html'
#     form_class = PersonaInvitadaForm
#     success_url = reverse_lazy('')

#     def get_context_data(self, **kwargs):
#         context = super(FormInvitadoCreate, self).get_context_data(**kwargs)
#         if 'form' not in context:
#             context['form'] = PersonaInvitadaForm(self.request.GET)
#         return context

#     @method_decorator(csrf_protect)
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Registrado correctamente")
#             return redirect("/registrologinpaciente/")
#             # return redirect("/registrologinpaciente/%s" %(persona.numero_documento))
#         else:
#             print('**********NO ENTRA***********')
#             messages.error(
#                 request, "No se registro correctamente, intentelo nuevamente")
#             return render(request, "inicio/login.html")


#------------------------------------------------------------------------------------------------------#
# Registro del Usuario Paciente que esta fuera de la WEB
#------------------------------------------------------------------------------------------------------#
def registrologin(request, cedula):
    context = {
        'form': UsuarioLoginForm()
    }
    if request.method == "POST":
        form = UsuarioLoginForm(request.POST)
        if form.is_valid():
            print('Cedula en registrologin', cedula)
            user = form.save(commit=False)
            persona = Persona.objects.get(numero_documento=cedula)
            grupo = Group.objects.get(name='Paciente')
            user.numero_documento = persona
            user.save()
            grupo.user_set.add(user)
            usuario = form.cleaned_data['usuario']
            messages.success(request, f'Usuario {usuario} creado ')
            context["mensaje"] = "Registrado correctamente"
            return redirect("/login/")
    else:
        form = UsuarioLoginForm()

    context = {'form': form}

    return render(request, 'inicio/registrologinpaciente.html', context)


'''CRUD de Usuario'''
#------------------------------------------------------------------------------------------------------#
# ***Views de Crear Usuario***


@permission_required('webapp.agregar_usuario', login_url="/panel_control/error/",)
def agregar_usuario(request):
    data = {
        'form': UsuarioForm()
    }
    if request.method == "POST":
        formulario = UsuarioForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Agregado")
            data["mensaje"] = "Registrado correctamente"
        else:
            data["form"] = formulario

    return render(request, "usuario/agregar_usuario.html", data)

    # funciona, vista simple de listar
# def listar_usuario(request):
#     listado_usuarios= Usuario.objects.all()

#     data={
#         'listado_usuarios':listado_usuarios
#     }

#     return render (request,"usuario/listar_usuario.html",data)
# funciona

# -----------------------------------------------------------------------------------------------
# ***Vista que Lista y busca--Funciona****


@permission_required('webapp.listar_usuario', login_url="/panel_control/error/")
def listar_usuario(request):

    busqueda = request.POST.get("q")
    listado_usuarios = Usuario.objects.all()

    if busqueda:
        listado_usuarios = Usuario.objects.filter(
            Q(usuario__icontains=busqueda))
        print("AQUI ESTA ENTRANDO Y buscando", {
              'listado_usuarios': listado_usuarios})
    else:

        print("Buscado AQUI",)
       # return render (request, "usuario/buscar.html")

    return render(request, "usuario/listar_usuario.html", {'listado_usuarios': listado_usuarios})

# -----------------------------------------------------------------------------------------------

# ***Vista de Modificar Usuario


@permission_required('webapp.modificar_usuario', login_url="/panel_control/error/",)
def modificar_usuario(request, usuario):
    usuario = Usuario.objects.get(usuario=usuario)

    data = {
        'form': UsuarioUpdateForm(instance=usuario)
    }
    if request.method == 'POST':
        formulario = UsuarioForm(
            data=request.POST, instance=usuario, files=request.FILES)
        if formulario.is_valid():

            formulario.save()
            formulario.save_m2m()
            data["form"] = formulario
            messages.success(request, " ✅Cambio realizado")

        else:
            messages.error(request, "Algo ha salido Mal ⚠️")

            # El return HttpResponse envia a otra pagina, he indica que se ha modificado la contraseña
            # return HttpResponse('"Modificado correctamente"')

        # data["form"] = formulario
        # print("pasa por aca y no toma el cambio!!!!!!!!!!!!!!!!!!!!!", formulario)
#             #se vuelve a cargar, dado que se actuliza arriba y debe volver a guardar
    return render(request, "usuario/modificar_usuario.html", data)


# -----------------------------------------------------------------------------------------------
# Vista de Modificar su propia contraseña
class UsuarioView(LoginMixin, View):
    template_name = 'usuario/modificar_password.html'
    form_class = PasswordUsuarioForm
    # success_url = reverse_lazy('panel_control')
    template_success = 'usuario/success.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        data = {
            'form': PasswordUsuarioForm()
        }
        if form.is_valid():
            user = Usuario.objects.filter(usuario=request.user.usuario)
            if user.exists():
                user = user.first()
                user.set_password(form.cleaned_data.get('password1'))
                user.save()
                data['mensaje'] = "modificada correctamente"
                update_session_auth_hash(request, user)
                # logout(request)
            #     return redirect(self.success_url)
                return render(request, self.template_success, data)
            # return HttpResponse('"Modificado correctamente"')
        else:
            form = self.form_class(request.POST)
            return render(request, self.template_name, {'form': form})


# -----------------------------------------------------------------------------------------------
# ***Vista de Eliminar Usuario
@permission_required('webapp.eliminar_usuario', login_url="/panel_control/error/",)
def eliminar_usuario(request, usuario):
    try:
        usuarios = Usuario.objects.get(usuario=usuario)
        usuarios.delete()
        listado_usuarios = Usuario.objects.all()
        #print ("usuario eliminado",{'listado_usuarios': listado_usuarios})
       # print("ESTA ES LA LISTA: ->",  context={'listado_usuarios': listado_usuarios})
        messages.success(request, "Eliminado")
        #messages.error(request, 'Este usuario ha sido eliminado ..!')
        return render(request, "usuario/listar_usuario.html", {'listado_usuarios': listado_usuarios})
        # return redirect(to="listar_usuario")
    except Usuario.DoesNotExist:
        message.error(request, "El usuario que quiere eliminar ya no existe")
        raise Http404(
            "No se puede eliminar el Usuario indicado. Dado que ya se Elimino")

# # ***Vista del Estado de Usuarios
# def estado_usuario(request):

#     listado_usuarios = Usuario.objects.all()

#     return render(request, "usuario/estado_usuario.html", {'listado_usuarios': listado_usuarios})


# Vista de Reset de PASSWORD mediante el correo

class ResetPasswordView(FormView):
    template_name = 'inicio/recuperar_pass.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('panel_control')
    # success_url = reverse_lazy(setting.LOGIN_REDIRECT_URL)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# def enviarcorreo(request):
#     if request.method == "POST":
#         subject = request.POST['asunto']
#         message = request.POST['mensaje'] + \
#             "|Remitente" + request.POST['correo']

#         email_from = settings.EMAIL_HOST_USER

#         recipient_list = ["psmilesoft@gmail.com"]

#         send_mail(subject, message, email_from, recipient_list)
#         print("entra aqui")
#         return redirect("enviarcorreo.html")

#     return render(request, "inicio/enviarcorreo.html")
