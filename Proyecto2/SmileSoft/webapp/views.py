from asyncio.windows_events import NULL
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
from .forms import UsuarioLoginForm
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
import webapp.gmail
from webapp.gmail import enviar_correo, enviar_link_reseteo
from django.contrib.auth.tokens import default_token_generator

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


#----------------------------------------------------PACIENTE--------------------------------------------------#

#------------------------------------------------------------------------------------------------------#
# Formulario de Registro de Paciente
class MensajeView(TemplateView):
    template_name= 'inicio/mensaje_redireccion.html'


class MensajeView2(TemplateView):
    template_name= 'inicio/mensaje_redireccion2.html'


def mostrar_confirmacion_usuario(request, cedula):
    context ={'cedula':cedula}
    return render(request, "inicio/confirmacion_usuario.html", context)

def resetear_password(request, cedula):
    persona = Persona.objects.get(numero_documento=cedula)
    email = persona.correo_electronico
    password = Usuario.objects.make_random_password()
    usuario = Usuario.objects.cambiar_password( password, cedula)
    nombre_usuario = usuario.usuario
    enviar_link_reseteo(email, nombre_usuario,password)
    return redirect('/password_reset_done/')


class PasswordResetDoneView(TemplateView):
    template_name= "inicio/password_reset_done.html"


class Mensaje_confirmacion(TemplateView):
    template_name= "inicio/mensaje_confirmacion.html"


def mostrar_mensaje_confirmacion(request, cedula):
    context ={'cedula':cedula}
    return render(request, "inicio/mensaje_confirmacion.html", context)


class CedulaConsultaView(TemplateView):
    template_name = "inicio/consultar_documento.html"
    form_class = ConsultaInvitadoForm
    
    def get_context_data(self, **kwargs):
        context = super(CedulaConsultaView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        return context

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # invitado = form.numero_documento
            cedula = form.cleaned_data['numero_documento']
            try: # Comprueba si esta registrado como paciente
                paciente = Paciente.objects.get(numero_documento=cedula)
            except ObjectDoesNotExist: # Si no es paciente muestra el siguiente mensaje
                return redirect("/mensaje")
            else: # Si es un paciente, comprueba si tiene un usuario
                try: 
                    usuario = Usuario.objects.get(numero_documento=cedula)
                except ObjectDoesNotExist: # Si no tiene un usuario pregunta si quiere generarlo
                    return redirect("/mensaje_confirmacion/%s" %(cedula))
                else: # Si el paciente ya tiene un usuario pregunta si quiere iniciar sesion
                    return redirect("/confirmacion_usuario/%s" %(cedula))
        else:
            print("No es validooooooooooooo")
            return self.render_to_response(self.get_context_data(form=form))


class CedulaConsultaView2(TemplateView):
    """ Solicita la Cedula de identidad de la persona y consulta en la base de datos
        si cuenta con un usuario.
        * Si no cuenta con un usuario muestra un mensaje informativo
        Si comprueba que cuenta con un usuario restablece su contraseña y se lo envia
        por correo electronico
    """
    template_name = "inicio/consultar_documento2.html"
    form_class = ConsultaInvitadoForm

    def get_context_data(self, **kwargs):
        context = super(CedulaConsultaView2, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        return context

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cedula = form.cleaned_data['numero_documento']
            try: # Comprueba si esta registrado como paciente
                usuario = Usuario.objects.get(numero_documento=cedula)
            except ObjectDoesNotExist: # Si no cuenta con un usuario muestra el siguiente mensaje
                return redirect("/mensaje_respuesta")
            else: # Si tiene un usuario
                return redirect("/password_reset/%s" %(cedula))
        else:
            print("No es validooooooooooooo")
            return self.render_to_response(self.get_context_data(form=form))


def generar_usuario_paciente(request, cedula):
    persona = Persona.objects.get(numero_documento=cedula)
    password = Usuario.objects.make_random_password()
    print('contraseña: ',password)
    usuario = Usuario.objects.create_user(password, cedula)
    grupo = Group.objects.get(name='Paciente')
    grupo.user_set.add(usuario)
    email = persona.correo_electronico
    context ={'cedula':cedula}

    if usuario:
        nombre_usuario = usuario.usuario
        enviar_correo(email,nombre_usuario,password)
        return render(request, "inicio/mensaje_envio_correo.html", context)

def generar_password(request, cedula):
    persona = Persona.objects.get(numero_documento=cedula)
    password = Usuario.objects.make_random_password()
    print('contraseña: ',password)
    usuario = Usuario.objects.cambiar_password(password, cedula)
    email = persona.correo_electronico
    context ={'cedula':cedula}
    if usuario:
        return render(request, "inicio/mensaje_envio_correo.html", context)


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


# @permission_required('webapp.agregar_usuario', login_url="/panel_control/error/",)
def agregar_usuario(request):
    data = {
        'form': UsuarioForm()
    }
    if request.method == "POST":
        formulario = UsuarioForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            # messages.success(request, "Agregado")
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


# @permission_required('webapp.listar_usuario', login_url="/panel_control/error/")
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


# @permission_required('webapp.modificar_usuario', login_url="/panel_control/error/",)
def modificar_usuario(request, usuario):
    usuario = Usuario.objects.get(usuario=usuario)

    data = {
        'form': UsuarioUpdateForm(instance=usuario),
        'object':Usuario.objects.get(usuario=usuario)
    }
    if request.method == 'POST':
        formulario = UsuarioUpdateForm(
            data=request.POST, instance=usuario, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            formulario._save_m2m()
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

def cambiar_password_usuario(request, usuario):
    usuario2 = Usuario.objects.get(usuario=usuario)
    data = {
        'form': UsuarioPassworUpdateForm(instance=usuario2),
        'object':usuario2
    }
    if request.method == 'POST':
        formulario = UsuarioPassworUpdateForm(
            data=request.POST, instance=usuario2, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            formulario._save_m2m()
            data["form"] = formulario
            messages.success(request, " ✅ Contraseña modificada")
            return redirect("/modificar_usuario/%s" %(usuario))
        else:
            messages.error(request, "Algo ha salido Mal ⚠️")
            # El return HttpResponse envia a otra pagina, he indica que se ha modificado la contraseña
            # return HttpResponse('"Modificado correctamente"')
        # data["form"] = formulario
        # print("pasa por aca y no toma el cambio!!!!!!!!!!!!!!!!!!!!!", formulario)
#             #se vuelve a cargar, dado que se actuliza arriba y debe volver a guardar
    return render(request, "usuario/cambiar_password_usuario.html", data)

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
# @permission_required('webapp.eliminar_usuario', login_url="/panel_control/error/",)
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