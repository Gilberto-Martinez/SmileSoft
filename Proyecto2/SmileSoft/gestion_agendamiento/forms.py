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

    # fecha = forms.DateField(
    #     label='Fecha', widget=forms.DateInput(attrs={'type': 'date'}))
    
    # hora = forms.DateTimeField(
    #     widget=forms.DateTimeInput(attrs={'type': 'time'}))

    class Meta:
        model= Cita
        fields= '__all__'
    
        # widgets = {
        #             'tratamiento_solicitado': forms.Select(attrs={
        #                                                     'class': 'form-select2',
        #                                                     'style': 'width: auto',
        #                                                     'multiple': 'multiple'
        #                                                 }), 
                
        #     }
