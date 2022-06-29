from dataclasses import field
from distutils import text_file
from email.headerregistry import Group
from re import U
from django.forms import BooleanField, CheckboxInput, CheckboxSelectMultiple, ModelForm, MultipleHiddenInput, PasswordInput, SelectMultiple, ValidationError, widgets
from tokenize import group
from django import forms
from .models import *
from django.contrib import messages
from django.http import request
from agregar_mas import *
from django.contrib.auth.models import Group, Permission, GroupManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.utils.translation import gettext as _, ngettext

#Import para el Login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm

from gestion_administrativo.models import PacienteTratamientoAsignado



#---------------------------------------------------------------------------------------- FORMULARIOS DEL CRUD DE USUARIO------------------------------------------------------------------------------------#
class InsumoForm(forms.ModelForm):
    nombre_insumo = forms.CharField( widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese el nombre del insumo'}))
    descripcion_insumo = forms.CharField( widget = forms.Textarea (attrs = {'class': 'form-control', 'placeholder': 'Breve descripción del insumo'}))
    precio = forms.IntegerField(
                                                   label='Precio', 
                                                   widget = forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': 'Ingrese el precio del insumo'}))
    fecha_caducidad = forms.DateField(label='Fecha de caducidad', widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Insumo
       # fields= '__all__'
        fields = [
            'codigo_insumo',
            'nombre_insumo',
            'descripcion_insumo',
            'precio',
            'fecha_caducidad',
            'estado',
        ]

class InsumoUpdateForm(forms.ModelForm):
    nombre_insumo = forms.CharField( widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese el nombre del insumo'}))
    descripcion_insumo = forms.CharField( widget = forms.Textarea (attrs = {'class': 'form-control', 'placeholder': 'Breve descripción del insumo'}))
    precio = forms.IntegerField(
                                                   label='Precio', 
                                                   widget = forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': 'Ingrese el precio del insumo'}))
    descripcion_insumo = forms.CharField( widget = forms.Textarea (attrs = {'class': 'form-control', 'placeholder': 'Breve descripción del insumo'} ))
    fecha_caducidad = forms.DateField(label='Fecha de caducidad', widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Insumo
       # fields= '__all__'
        fields = [
            'codigo_insumo',
            'nombre_insumo',
            'descripcion_insumo',
            'precio',
            'fecha_caducidad',
            'estado',
        ]

