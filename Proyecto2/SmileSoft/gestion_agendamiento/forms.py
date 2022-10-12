from datetime import timedelta
from tkinter import Widget
from tokenize import _all_string_prefixes
from gestion_administrativo.models import Paciente
from django import forms
from webapp.models import Usuario
from .models import *
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import widgets
from datetime import datetime
import datetime


class CitaForm(forms.ModelForm):
    fecha_meses = (datetime.date.today())+ timedelta(365/2)
    fecha = forms.DateField(
        label='Fecha de consulta:', widget=forms.NumberInput(attrs={'type': 'date', 'min': "2022-01-01" ,'max': str(fecha_meses)}))
    
    # hora = forms.TimeField(label='Hora de cita: ',
    #                        help_text='<small> <b>Lunes a Viernes</b>  ! <br> 08:00hs a 12:00hs ; 13:30hs a 21:00hs </i></small>',
    #     widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model= Cita
        fields= [
                'tratamiento_solicitado',
                'fecha',
                # 'hora',
                'hora_atencion',
                'profesional',
                'estado',
        ]


class CitaForm2(forms.ModelForm):
    fecha = forms.DateField(
        label='Fecha de consulta: ', widget=forms.NumberInput(attrs={'type': 'date'}))
    
    # hora = forms.TimeField(label='Hora de cita: ',
    #                        help_text='<small> <b>Lunes a Viernes</b>  ! <br> 08:00hs a 12:00hs ; 13:30hs a 21:00hs </i></small>',
    #     widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model= Cita
        fields= [
              #  'tratamiento_solicitado',
                'fecha',
                # 'hora',
                'hora_atencion',
                
                'profesional',
                'estado',
        ]
      
class CitaUsuario(forms.ModelForm):
    fecha = forms.DateField(
        label='Fecha de consulta: ', widget=forms.NumberInput(attrs={'type': 'date', 'readonly': True}))
    
    # hora = forms.TimeField(label='Hora',
    #                        help_text='<small> <b>Lunes a Viernes</b>  ! <br> 08:00hs a 12:00hs ; 13:30hs a 21:00hs </i></small>',
    #                        widget=forms.TimeInput(attrs={'type': 'time', 'readonly': True}))
    
    
    
    class Meta:
        model= Cita
        fields= [
                'tratamiento_solicitado',
                'fecha',
                # 'hora',
                'hora_atencion',
                'profesional',
                'estado',
        ]
    

class HoraForm (forms.ModelForm):
    hora = forms.TimeField(label='Hora de cita: ',
                           widget=forms.TimeInput(attrs={'type': 'time'}))
    class Meta:
        model= Horario
        fields=['hora',
                # 'dias_atencion'
        ]