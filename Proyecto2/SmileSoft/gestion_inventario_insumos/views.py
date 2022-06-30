from django.shortcuts import render

# Create your views here.
from email import quoprimime
from email.charset import QP
from tokenize import Name
from unicodedata import name
from django.shortcuts import render
from urllib3 import encode_multipart_formdata
#from Proyecto2.SmileSoft.gestion_inventario_insumos.models import Insumo
# from gestion_roles.models import Rol
from gestion_roles.forms import *
from webapp.forms import *
#from .forms import *
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
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DeleteView, DetailView
from gestion_administrativo.forms import *
from gestion_inventario_insumos.forms import *

# ***Vista de Agregar Rol
# @permission_required('gestion_inventario_insumos.agregar_insumo', login_url="/panel_control/error/",)
def agregar_insumo (request):
    
    data= {
        'form' : InsumoForm()
    }
    
    if request.method== "POST":
        formulario= InsumoForm(data = request.POST, files= request.FILES)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"]="Registrado correctamente"
            messages.success(request, (
                'Agregado correctamente!'))
            print('aquiiiiiiiiiiiiii ENTRAAAAA')
        else:
            data["form"]=formulario
            print('NO ENTRAAAAA')
            
    return render(request,"insumo/agregar_insumo.html",data)

# -----------------------------------------------------------------------------------------------
# ***Vista de listar Insumo


# @permission_required('gestion_inventario_iinsumos.listar_insumo', login_url="/panel_control/error/",)
def listar_insumo(request):
    
    busqueda=request.POST.get("q")
    listado_insumos = Insumo.objects.all()
    
    if busqueda:  
        listado_insumos =Insumo.objects.filter(Q(nombre_insumo__icontains= busqueda))
        print("AQUI ESTA ENTRANDO Y buscando", {'listado_insumos':listado_insumos})
    else:                                                              
        print("Buscado AQUI",)
        
    return render (request,"insumo/listar_insumos.html",{'listado_insumos':listado_insumos})

# -----------------------------------------------------------------------------------------------

# ***Vista de Modificar Insumos


# @permission_required('gestion_tratamiento.modificar_tratamiento', login_url="/panel_control/error/",)
def modificar_insumo(request, nombre_insumo):
    nombre_insumo = Insumo.objects.get(nombre_insumo=nombre_insumo)

    data= {
        'form': InsumoUpdateForm(instance=nombre_insumo)
    }
    if request.method == 'POST':
        formulario = InsumoForm(
            data=request.POST, instance=nombre_insumo, files=request.FILES)
        if formulario.is_valid():
            
            formulario.save()
            
            messages.success(request, "Modificado")       
            print("ENTRA AQUI !!!!!!!!!!!!!!!!!!!!!")
                  
            data['mensaje'] = "Modificado correctamente"
            
        else:
            messages.error(request, "Algo ha salido Mal, por favor verifique nuevamente")
            print("NOOOOOOOOOOO modifica!!!!!!!!!!!!!!!!!!!!!")

    return render(request, "insumo/modificar_insumos.html", data)


# -----------------------------------------------------------------------------------------------
# ***Vista de Eliminar Insumo
# @permission_required('gestion_inventario_insumo.eliminar_insumo', login_url="/panel_control/error/",)
def eliminar_insumo(request, nombre_insumo):
    try:
        insumo = Insumo.objects.get(nombre_insumo=nombre_insumo)
        insumo.delete()
        listado_insumos = Insumo.objects.all()
        messages.success(request, "Eliminado")
        return render(request, "insumo/listar_insumos.html", {'listado_insumos': listado_insumos})
    except Insumo.DoesNotExist:
        raise Http404("No se puede eliminar el Insumo indicado. Dado que ya se Elimino")