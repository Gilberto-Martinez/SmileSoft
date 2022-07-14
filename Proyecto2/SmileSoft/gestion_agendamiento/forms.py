from tkinter import Widget
from tokenize import _all_string_prefixes
from gestion_administrativo.models import Paciente
from django import forms
from webapp.models import Usuario
from .models import *
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import widgets


class CitaForm(forms.ModelForm):
    # fecha: forms.DateField(widget=widgets.AdminDateWidget())
    # tratamiento_solicitado = forms.CharField( widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese el motivo de la consulta',}))

    fecha = forms.DateField(
        label='Fecha de consulta: ', widget=forms.NumberInput(attrs={'type': 'date'}))
    
    hora = forms.TimeField(label='Hora de cita: ',
        widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model= Cita
        fields= [
                'tratamiento_solicitado',
                'fecha',
                'hora',
        ]
    
        # widgets = {
        #             'tratamiento_solicitado': forms.Select(attrs={
        #                                                     'class': 'form-select2',
        #                                                     'style': 'width: auto',
        #                                                     'multiple': 'multiple'
        #                                                 }), 
                
        #     }
