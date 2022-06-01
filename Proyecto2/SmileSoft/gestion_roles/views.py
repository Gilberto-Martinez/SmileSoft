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
from django.contrib.auth.decorators import login_required, permission_required


# ***Vista de Agregar Rol
@permission_required('gestion_roles.agregar_rol', login_url="/panel_control/error/",)
def agregar_rol(request):

    data = {
        'form': RolForm()
    }

    if request.method == "POST":
        formulario = RolForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Registrado correctamente"
            messages.success(request, (
                'Agregado correctamente!'))
            print('aquiiiiiiiiiiiiii ENTRAAAAA')
        else:
            data["form"] = formulario
            print('NO ENTRAAAAA')

    return render(request, "roles/agregar_roles.html", data)

# -----------------------------------------------------------------------------------------------
# ***Vista de listar Roles


@permission_required('gestion_roles.listar_roles', login_url="/panel_control/error/",)
def listar_roles(request):

    busqueda = request.POST.get("q")
    listado_roles = Group.objects.all()

    if busqueda:
        listado_roles = Group.objects.filter(Q(name__icontains=busqueda))
        print("AQUI ESTA ENTRANDO Y buscando",
              {'listado_roles': listado_roles})
    else:
        print("Buscado AQUI",)
       # return render (request, "roles/buscar.html")

    return render(request, "roles/listar_roles.html", {'listado_roles': listado_roles})

# -----------------------------------------------------------------------------------------------

# ***Vista de Modificar Rol


@permission_required('gestion_roles.modificar_rol', login_url="/panel_control/error/",)
def modificar_rol(request, name):
    name = Group.objects.get(name=name)

    data = {
        'form': RolUpdateForm(instance=name)
    }
    if request.method == 'POST':
        formulario = RolForm(
            data=request.POST, instance=name, files=request.FILES)
        if formulario.is_valid():

            formulario.save()

            messages.success(request, "Modificado")
            print("ENTRA AQUI !!!!!!!!!!!!!!!!!!!!!")

            data['mensaje'] = "Modificado correctamente"

        else:
            messages.error(
                request, "Algo ha salido Mal, por favor verifique nuevamente")
            print("NOOOOOOOOOOO modifica!!!!!!!!!!!!!!!!!!!!!")

    return render(request, "roles/modificar_rol.html", data)


# -----------------------------------------------------------------------------------------------
# ***Vista de Eliminar Rol
@permission_required('gestion_roles.eliminar_rol', login_url="/panel_control/error/",)
def eliminar_rol(request, name):
    try:
        roles = Group.objects.get(name=name)
        roles.delete()
        listado_roles = Group.objects.all()
        #print ("usuario eliminado",{'listado_usuarios': listado_usuarios})
       # print("ESTA ES LA LISTA: ->",  context={'listado_usuarios': listado_usuarios})
        messages.success(request, "Eliminado")
        #messages.error(request, 'Este usuario ha sido eliminado ..!')
        return render(request, "roles/listar_roles.html", {'listado_roles': listado_roles})
        # return redirect(to="listar_usuario")
    except Usuario.DoesNotExist:
        # message.error(request, "El usuario que quiere eliminar ya no existe")
        raise Http404(
            "No se puede eliminar el Usuario indicado. Dado que ya se Elimino")
