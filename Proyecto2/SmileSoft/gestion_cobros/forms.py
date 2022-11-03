from dataclasses import field, fields
from pyexpat import model
from django import forms
from .models import *

# class CobroContadoForm(forms.ModelForm):
#     paciente = forms.CharField(widget=forms.TextInput(attrs={
#                                                         'class': 'form-control',
#                                                             'placeholder': 'Ingrese su nombre'
#                                                             }
#                                                     )
#                                 )
#     numero_documento = forms.CharField(widget=forms.TextInput(attrs={
#                                                             'class': 'form-control',
#                                                             'placeholder': 'Ingrese su nombre'
#                                                             }
#                                                     )
#                                 )
#     razon_social = forms.CharField(widget=forms.TextInput(attrs={
#                                                             'class': 'form-control',
#                                                             'placeholder': 'Ingrese su nombre'
#                                                             }
#                                                     )
#                                 )
#     fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
#     monto_total = forms.IntegerField(widget=forms.NumberInput(attrs={
#                                                                     'class': 'form-control',
#                                                                     'placeholder': 'Ingrese su nombre'
#                                                                     }
#                                                             )
#                                     )
#     class Meta:
#         model = CobroContado
#         fields = [
#                     'paciente',
#                     'numero_documento',
#                     'razon_social',
#                     'fecha',
#                     'monto_total',
#         ]

class RazonSocialForm(forms.ModelForm):
    numero_documento = forms.CharField(widget=forms.TextInput(attrs={
                                                            'class': 'form-control',
                                                            'placeholder': 'Ingrese su nombre'
                                                            }
                                                    )
                                )
    razon_social = forms.CharField(widget=forms.TextInput(attrs={
                                                            'class': 'form-control',
                                                            'placeholder': 'Ingrese su nombre'
                                                            }
                                                    )
                                )

    class Meta:
        model = CobroContado
        fields = [
                    'numero_documento',
                    'razon_social',
        ]