from django.shortcuts import render
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DeleteView

from .forms import *
# Create your views here.
from django.contrib import messages
from django.http import (
    Http404, HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect,)

#---------Vista Principal-------
def calendario(request):
    return render(request, "calendario.html")


#<--Agregar cita-->

def agregar_cita(request):

    data = {
        'form': CitaForm()
    }

    if request.method == "POST":
        formulario = CitaForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Registrado correctamente"
            messages.success(request, (
                'Agregado correctamente!'))
            print('aquiiiiiiiiiiiiii ENTRAAAAA')
        else:
            messages.error(request, (
                'No ha guardado'))
            data["form"] = formulario
            print('NO ENTRAAAAA')

    return render(request, "agregar_cita.html", data)


#<--Modificar cita-->

def modificar_cita(request, id_cita):
    paciente = Paciente.objects.get(id_cita=id_cita)

    data = {
        'form': CitaForm(instance=paciente)
    }

    if request.method == "POST":
        formulario = CitaForm(
            data=request.POST, instance=paciente, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Cita Modificada"
            messages.success(request, (
                'Modificado correctamente!'))
            print('aquiiiiiiiiiiiiii ENTRAAAAA')
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

        messages.success(request, "Eliminado")

    except Usuario.DoesNotExist:
        # message.error(request, "El usuario que quiere eliminar ya no existe")
        raise Http404(
            "No se puede eliminar la cita indicada. Dado que ya se Elimino")
