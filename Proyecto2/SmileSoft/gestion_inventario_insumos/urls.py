from django.urls import path
from .views import *
from django.urls import path
from .views import *
from gestion_administrativo import *
from audioop import reverse
from multiprocessing import context
from pyexpat import model
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .forms import *
from django.contrib import messages
from django.views.generic import ListView,CreateView, TemplateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from gestion_administrativo.views import PacienteList2
from gestion_administrativo.views import *
from django.views.generic import ListView,CreateView, TemplateView, UpdateView, DeleteView
urlpatterns = [
            path('listar_insumo/', listar_insumo, name="listar_tratamiento"),
            path('eliminar_insumo/<nombre_insumo>/', eliminar_insumo, name="eliminar_insumo"),
            path('agregar_insumo/', agregar_insumo, name="agregar_insumo"),
            path('modificar_insumos/<nombre_insumo>/', modificar_insumo, name="modificar_insumos"),          
            path('listar_paciente2/', PacienteList2.as_view(),  name="listar_paciente2"),
            
            
]