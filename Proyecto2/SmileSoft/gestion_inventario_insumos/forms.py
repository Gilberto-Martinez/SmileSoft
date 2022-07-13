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
    nombre_insumo = forms.CharField(label='Nombre del Insumo', widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese el nombre del insumo'}))
    descripcion_insumo = forms.CharField(label='Descripción del Insumo', widget = forms.Textarea (attrs = {'class': 'form-control', 'placeholder': 'Breve descripción del insumo'}))
    precio = forms.IntegerField(
                                                   label='Precio', 
                                                   widget = forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': 'Ingrese el precio del insumo'}))
    fecha_caducidad = forms.DateField(label='Fecha de caducidad', widget=forms.DateInput(attrs={'type': 'date'}))
    cantidad_insumo = forms.IntegerField(
                                                   label='Cantidad del Insumo', 
                                                   widget = forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': 'Ingrese la cantidad del insumo'}))
    class Meta:
        model = Insumo
       # fields= '__all__'
        fields = [
            'codigo_insumo',
            'nombre_insumo',
            'descripcion_insumo',
            'precio',
            'fecha_caducidad',
            'cantidad_insumo'
            #'estado',
        ]

class InsumoUpdateForm(forms.ModelForm):
    nombre_insumo = forms.CharField(label='Nombre del Insumo', widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese el nombre del insumo'}))
    descripcion_insumo = forms.CharField(label='Descripción del Insumo', widget = forms.Textarea (attrs = {'class': 'form-control', 'placeholder': 'Breve descripción del insumo'}))
    precio = forms.IntegerField(
                                                   label='Precio', 
                                                   widget = forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': 'Ingrese el precio del insumo'}))
    fecha_caducidad = forms.DateField(label='Fecha de caducidad', widget=forms.NumberInput(attrs={'type': 'date'}))
    cantidad_insumo = forms.IntegerField(
                                                   label='Cantidad del Insumo', 
                                                   widget = forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': 'Ingrese la cantidad del insumo'}))
    class Meta:
        model = Insumo
        fields= '__all__'
        # fields = [
        #     'codigo_insumo',
        #     'nombre_insumo',
        #     'descripcion_insumo',
        #     'precio',
        #     'fecha_caducidad',
        #     'cantidad_insumo'
        #     'estado',
        # ]

    def clean_fecha_caducidad(self):
        fecha_caducidad = self.cleaned_data["fecha_caducidad"]
        print(fecha_caducidad)
        fecha_caducidad = str(fecha_caducidad) # Convertir a str

        # fecha = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
        # edad = relativedelta(datetime.now(), fecha)
        # edad = edad.years
        # print(edad+ "años")

        # if edad < 18:
        #     # print ("La persona es menor de edad, no puede ser un funcionario")
        #     self.evento = "Menor de edad"
        #     self.mensaje_error = "La persona es menor de edad, no puede ser un funcionario"
        #     raise forms.ValidationError('La persona es menor de edad, no puede ser un funcionario')
        # else:
            # return fecha_nacimiento


    # def get_codigo_insumo(self):
    #     return self.codigo_insumo