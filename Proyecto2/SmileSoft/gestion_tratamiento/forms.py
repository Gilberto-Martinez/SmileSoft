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
from gestion_inventario_insumos.models import *



#---------------------------------------------------------------------------------------- FORMULARIOS DEL CRUD DE USUARIO------------------------------------------------------------------------------------#
class TratamientoForm(forms.ModelForm):
    nombre_tratamiento = forms.CharField( 
                                        label='Nombre del tratamiento',
                                        widget = forms.TextInput (attrs = {
                                                                            'class': 'form-control', 
                                                                            'placeholder': 'Ingrese el nombre del trataniento'
                                                                        }
                                                                )
                                        )
    descripcion_tratamiento = forms.CharField( 
                                            label='Descripción',
                                            widget = forms.Textarea (attrs = {
                                                                                'class': 'form-control', 
                                                                                'placeholder': 'Breve descripción del tratamiento'
                                                                            }
                                                                    )
                                            )
    precio = forms.IntegerField(
                                label='Precio', 
                               widget = forms.NumberInput(attrs = {
                                                                    'class': 'form-control', 
                                                                    'placeholder': 
                                                                    'Ingrese el precio del tratamiento'
                                                                }
                                                        )
                                )
    class Meta:
        model = Tratamiento
       # fields= '__all__'
        fields = [
            'codigo_tratamiento',
            'nombre_tratamiento',
            'descripcion_tratamiento',
            'precio',
            # 'insumos'
        ]
        # widgets = {
        #        'insumos': forms.CheckboxSelectMultiple(attrs={
        #        'class': 'form-select2',
        #        'style': 'width: 30px',
        #        'multiple': 'multiple'}),
        #        }

class TratamientoUpdateForm(forms.ModelForm):
    nombre_tratamiento = forms.CharField( 
                                        label='Nombre del tratamiento',
                                        widget = forms.TextInput (attrs = {
                                                                            'class': 'form-control',
                                                                            'placeholder': 'Ingrese el nombre del trataniento'
                                                                            }
                                                                )
                                        )
    descripcion_tratamiento = forms.CharField( 
                                            label='Descripción',
                                            widget = forms.Textarea (attrs = {
                                                                                'class': 'form-control',
                                                                                'placeholder': 'Breve descripción del tratamiento'
                                                                            }
                                                                    )
                                            )
    precio = forms.IntegerField(
                                label='Precio', 
                                widget = forms.NumberInput(attrs = {
                                                                    'class': 'form-control', 
                                                                    'placeholder': 'Ingrese el precio del tratamiento'
                                                                    }
                                                            )
                                )
    # descripcion_tratamiento = forms.CharField( widget = forms.Textarea (attrs = {'class': 'form-control', 'placeholder': 'Breve descripción del tratamiento'} ))
    class Meta:
        model = Tratamiento
       # fields= '__all__'
        fields = [
            'codigo_tratamiento',
            'nombre_tratamiento',
            'descripcion_tratamiento',
            'precio',
        ]

# class TratamientoInsAsignadoForm(forms.ModelForm):
#    class Meta:
#       model = Tratamiento
#       fields = [
#                'insumos',
#                 ]
#       widgets = {
#           'insumos': forms.CheckboxSelectMultiple(attrs={
#               'class': 'form-select2',
#               'style': 'width: 30px',
#               'multiple': 'multiple'}),
#                #  'numero_documento': HiddenInput(attrs={'required': False}
#                }
      # InlineForeignKeyField(Cargo)
   
      # label = 'Nombre de los tratamientos'