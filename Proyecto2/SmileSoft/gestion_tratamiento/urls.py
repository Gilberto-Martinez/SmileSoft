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
            path('listar_tratamiento/', listar_tratamiento, name="listar_tratamiento"),
            path('eliminar_tratamiento/<nombre_tratamiento>/', eliminar_tratamiento, name="eliminar_tratamiento"),
            path('agregar_tratamiento/', agregar_tratamiento, name="agregar_tratamiento"),
            path('modificar_tratamiento/<nombre_tratamiento>/', modificar_tratamiento, name="modificar_tratamiento"),          
            path('listar_paciente2/', PacienteList2.as_view(),  name="listar_paciente2"),
            # path('asignar_tratamiento/', asignar_tratamiento, name="asignar_tratamiento"),
            path('tratamientos_asignados/<int:pk>', DetalleTratamientosAsignados.as_view(), name="tratamientos_asignados"),
]