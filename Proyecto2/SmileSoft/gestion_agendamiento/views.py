from ctypes.wintypes import PCHAR
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DeleteView
from gestion_administrativo.forms import PersonaPacienteForm
from gestion_administrativo.forms import PersonaUpdateForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from webapp.mixins import LoginMixin
from django.db.models import Q
from .forms import *
# Create your views here.
from django.contrib import messages
from django.http import (
    Http404, HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect,)
from django.contrib.auth.decorators import permission_required
# ---------Vista Principal-------


class Calendario(LoginMixin, ListView):
    model = Cita
    template_name = 'calendar.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(
            estado=True)
        return queryset

# def calendario_vista(request):
#     return render(request, "calendario.html")
# def pruebacalendar(request):
#     return render(request, "calendar.html")


# <--Agregar cita-->

def agregar_cita(request, id_paciente):
    paciente = Paciente.objects.get(id_paciente=id_paciente)
    cedula = paciente.numero_documento
    persona = Persona.objects.get(numero_documento=cedula)
    nombre = persona.nombre + ' ' + persona.apellido
    # apellido = persona.apellido
    data = {
        'form': CitaForm(),
        'persona': persona
    }

    if request.method == "POST":
        formulario = CitaForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            cita = formulario.save(commit=False)
            cita.paciente = paciente
            cita.nombre_paciente = nombre
            # cita.apellido = apellido
            cita.save()
            # formulario.save()
            data["mensaje"] = "Registrado correctamente"
            messages.success(request, (
                'Agregado correctamente!'))
            print('aquiiiiiiiiiiiiii ENTRAAAAA')
            return redirect("/agendamiento/listado_citas/")
        else:
            messages.error(request, (
                'No ha guardado'))
            data["form"] = formulario
            print('NO ENTRAAAAA')

    return render(request, "agregar_cita.html", data)


# <--Agregar cita a UN USUARIO
def addcita_usuario(request, numero_documento):
    persona = Persona.objects.get(numero_documento=numero_documento)
    cedula = persona.numero_documento
    paciente = Paciente.objects.get(numero_documento=cedula)
    id_paciente = paciente.id_paciente
    nombre = persona.nombre + ' ' + persona.apellido
    # apellido = persona.apellido
    print('Esta es la cedula', cedula, 'Este es el id del paciente', id_paciente)

    data = {
        'form': CitaForm(),
        'persona': persona,
        'id_paciente': id_paciente
    }

    if request.method == "POST":
        formulario = CitaForm(data=request.POST, files=request.FILES)

        if formulario.is_valid():
            cita = formulario.save(commit=False)
            cita.paciente = paciente
            cita.nombre_paciente = nombre
            cita.save()
            messages.success(request, (
                '✅ Su cita ha sido registrada'))

            return render(request, "calendario.html")
        else:
            messages.error(request, (
                'No ha guardado'))
            data["form"] = formulario
            print('NO ENTRAAAAA')

    return render(request, "usuario_addCita.html", data)

# --> Esta es una template de redirección para el calendario


def calendario_vista(request):
    return render(request, "calendar.html")

# <- Modificar Cita del Usuario iniciado


def mis_citas_lista(request, numero_documento):
    #no funciona
    persona = Persona.objects.get(numero_documento=numero_documento)
    cedula = persona.numero_documento
    paciente = Paciente.objects.get(numero_documento=cedula)
    id_paciente = paciente.id_paciente
    
    cita = Cita.objects.get(paciente=cedula)
    
    pkcita = cita.id_cita
    
    mis_citas=Cita.objects.all()
    print('Imprime esto', {'mis_citas': mis_citas})
    
    return render(request, "mis_citas.html", {'mis_citas': mis_citas})


# @permission_required('gestion_agendamiento.cambiarCita_usuario', login_url="/panel_control/error/",)
def cambiarCita_usuario(request, id_cita):
#enproceso
    cita = Cita.objects.get(id_cita=id_cita)
    cedula = cita.paciente
    persona = Persona.objects.get(numero_documento=cedula)
    ci_persona= persona.numero_documento
    ci_user= Usuario.objects.get(numero_documento=ci_persona)
    nro_documento=ci_user.numero_documento
    persona_user=ci_user.usuario
    # user = Usuario.objects.filter(usuario=request.user.usuario)
    # cedula_user=user.usuario
            
   
    nombre = persona.nombre + ' ' + persona.apellido

    data = {
        'form': CitaForm(instance=cita),
        'persona': persona,
        'id_cita': id_cita,
        'ci_user':ci_user,
        'nro_documento': nro_documento,
        # 'cedula_user':cedula_user
        
    }
    if request.method == "POST":
        formulario = CitaForm(
            data=request.POST, instance= cita,files=request.FILES)
        
        if formulario.is_valid():
            # user = Usuario.objects.filter(usuario=request.user.usuario)
            if persona_user == request.user.usuario:
                print('-------------------AQUI', persona_user,request.user.usuario)
                formulario.save()
                messages.success(request, (
                            '✅ Su cita ha sido modificada'))
                    
                return render(request, "calendario.html")
            else:
                messages.info(
                       request, "⚠️No está permitido modificar otra cita, que no sea la suya")
                return render(request, "panel_control/error.html")
            
               
                
        else:
                messages.error(request, (
                    'No ha guardado'))
                data["form"] = formulario
                print('NO ENTRAAAAA')
        # else:
        #     return render(request, "panel_control/error.html")

    return render(request, "usuario_changeCita.html", data)


# <--Modificar cita-->

def modificar_cita(request, id_cita):
    cita = Cita.objects.get(id_cita=id_cita)
    cedula = cita.paciente
    persona = Persona.objects.get(numero_documento=cedula)
    data = {
        'form': CitaForm(instance=cita),
        'persona': persona
    }

    if request.method == "POST":
        formulario = CitaForm(
            data=request.POST, instance=cita, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Cita Modificada"
            messages.success(request, (
                'Modificado correctamente!'))
            return redirect("/agendamiento/listado_citas/")
        else:
            messages.error(
                request, "Algo ha salido Mal, por favor verifique nuevamente")
    return render(request, "modificar_cita.html", data)

# <--Eliminar cita-->
def eliminar_cita(request, id_cita):
    try:
        citas = Cita.objects.get(id_cita=id_cita)
        citas.delete()
        listado_citas = Cita.objects.all()

        messages.success(request, "Eliminado")

        return render(request, "listado_citas.html", {'listado_citas': listado_citas})

    except Cita.DoesNotExist:
        raise Http404(
            "No se puede eliminar la cita indicada. Dado que ya se Elimino")
        
#Eliminar la cita de un usuario
def deletecita(request,id_cita):
    try:
       
        cita = Cita.objects.get(id_cita=id_cita)
        cedula = cita.paciente
        persona = Persona.objects.get(numero_documento=cedula)
        ci = persona.numero_documento
        ci_user = Usuario.objects.get(numero_documento=ci)
        if (ci_user == cedula):
            cita.delete()       
            return render(request, "delete_cita.html")
        else:
            messages.info(request, "⚠️Lamentamos informarle que NO puede eliminar otra cita que no sea la suya")
            return render(request, "panel_control/error.html")  
    except Cita.DoesNotExist:
        raise Http404(
            "No se puede eliminar la cita indicada. Dado que ya se Elimino")


# <--listado de los pacientes para agendar una cita
def listar_citapaciente(request):
    busqueda = request.POST.get("q")
    paciente_cita = Paciente.objects.all()

    if busqueda:

        paciente_cita = Paciente.objects.filter(
            numero_documento__in=[busqueda])
        # queryset = queryset.filter(nombre__contains=Q, apellido__contains=Q)
        # print("AQUI ESTA ENTRANDO", queryset)

    return render(request, "pacientes_cita.html", {
        'paciente_cita': paciente_cita})

# <-Listar cita AGENDADA-->
def listar_cita(request):
    busqueda = request.POST.get("q")
    listado_cita = Cita.objects.all()

    if busqueda:
        listado_cita = Cita.objects.filter(
            Q(nombre_paciente__icontains=busqueda))
        print("AQUI ESTA ENTRANDO Y buscando", {
              'listado_cita': listado_cita})
    else:
        print("Buscado AQUI",)
       # return render (request, "usuario/buscar.html")
    return render(request, "listado_citas.html", {
        'listado_cita': listado_cita,
    }
    )
