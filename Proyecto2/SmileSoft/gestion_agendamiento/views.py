from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DeleteView
from gestion_administrativo.forms import PersonaPacienteForm
from gestion_administrativo.forms import PersonaUpdateForm

from webapp.mixins import LoginMixin
from django.db.models import Q
from .forms import *
# Create your views here.
from django.contrib import messages
from django.http import (
    Http404, HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect,)

#---------Vista Principal-------


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


#<--Agregar cita-->

def agregar_cita(request, id_paciente):
    paciente = Paciente.objects.get(id_paciente=id_paciente)
    cedula = paciente.numero_documento
    persona = Persona.objects.get(numero_documento=cedula)
    nombre = persona.nombre +' '+ persona.apellido
    # apellido = persona.apellido
    data = {
        'form': CitaForm(),
        'persona':persona
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

#<-Listar cita-->
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
#<--Modificar cita-->

def modificar_cita(request,id_cita):
    cita = Cita.objects.get(id_cita= id_cita)
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

            print('NO ENTRAAAAA')

    return render(request, "modificar_cita.html", data)

#<--Eliminar cita-->

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



def listar_citapaciente(request):
    busqueda = request.POST.get("q")
    paciente_cita= Paciente.objects.all()
  
    if busqueda:
       
        paciente_cita = Paciente.objects.filter(numero_documento__in=[busqueda])
        # queryset = queryset.filter(nombre__contains=Q, apellido__contains=Q)
        # print("AQUI ESTA ENTRANDO", queryset)
                
    return render(request, "pacientes_cita.html", {
        'paciente_cita': paciente_cita})