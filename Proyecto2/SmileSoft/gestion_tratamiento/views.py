from django.shortcuts import render

# Create your views here.
from email import quoprimime
from email.charset import QP
from tokenize import Name
from unicodedata import name
from django.shortcuts import render
# from gestion_roles.models import Rol
from gestion_roles.forms import *
from webapp.forms import *
from .forms import *
from django.contrib import messages
from django.http import (
    Http404, HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect,)
from django.views.generic.list import ListView
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db.models import Q 
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import permission_required

# ***Vista de Agregar Rol
@permission_required('gestion_tratamiento.agregar_tratamiento', login_url="/panel_control/error/",)
def agregar_tratamiento (request):
    
    data= {
        'form' : TratamientoForm()
    }
    
    if request.method== "POST":
        formulario= TratamientoForm(data = request.POST, files= request.FILES)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"]="Registrado correctamente"
            messages.success(request, (
                'Agregado correctamente!'))
            print('aquiiiiiiiiiiiiii ENTRAAAAA')
        else:
            data["form"]=formulario
            print('NO ENTRAAAAA')
            
    return render(request,"tratamiento/agregar_tratamiento.html",data)

# -----------------------------------------------------------------------------------------------
# ***Vista de listar Tratamiento


# @permission_required('gestion_tratamiento.listar_tratamiento', login_url="/panel_control/error/",)
def listar_tratamiento(request):
    
    busqueda=request.POST.get("q")
    listado_tratamientos = Tratamiento.objects.all()
    
    if busqueda:  
        listado_tratamientos =Tratamiento.objects.filter(Q(nombre_tratamiento__icontains= busqueda))
        print("AQUI ESTA ENTRANDO Y buscando", {'listado_tratamientos':listado_tratamientos})
    else:                                                              
        print("Buscado AQUI",)
        
    return render (request,"tratamiento/listar_tratamientos.html",{'listado_tratamientos':listado_tratamientos})

# -----------------------------------------------------------------------------------------------

# ***Vista de Modificar Rol


@permission_required('gestion_tratamiento.modificar_tratamiento', login_url="/panel_control/error/",)
def modificar_tratamiento(request, nombre_tratamiento):
    nombre_tratamiento = Tratamiento.objects.get(nombre_tratamiento=nombre_tratamiento)

    data= {
        'form': TratamientoUpdateForm(instance=nombre_tratamiento)
    }
    if request.method == 'POST':
        formulario = TratamientoForm(
            data=request.POST, instance=nombre_tratamiento, files=request.FILES)
        if formulario.is_valid():
            
            formulario.save()
            
            messages.success(request, "Modificado")       
            print("ENTRA AQUI !!!!!!!!!!!!!!!!!!!!!")
                  
            data['mensaje'] = "Modificado correctamente"
            
        else:
            messages.error(request, "Algo ha salido Mal, por favor verifique nuevamente")
            print("NOOOOOOOOOOO modifica!!!!!!!!!!!!!!!!!!!!!")

    return render(request, "tratamiento/modificar_tratamiento.html", data)


# -----------------------------------------------------------------------------------------------
# ***Vista de Eliminar Tratamiento
@permission_required('gestion_tratamiento.eliminar_tratamiento', login_url="/panel_control/error/",)
def eliminar_tratamiento(request, nombre_tratamiento):
    try:
        tratamiento = Tratamiento.objects.get(nombre_tratamiento=nombre_tratamiento)
        tratamiento.delete()
        listado_tratamientos = Tratamiento.objects.all()
        messages.success(request, "Eliminado")
        return render(request, "tratamiento/listar_tratamientos.html", {'listado_tratamientos': listado_tratamientos})
    except Tratamiento.DoesNotExist:
        raise Http404("No se puede eliminar el Tratamiento indicado. Dado que ya se Elimino")



# class TratamientoDelete(DeleteView):
#     model = Tratamiento
#     template_name = 'eliminar_tratamiento.html'
#     success_url = reverse_lazy('listar_tratamientos')