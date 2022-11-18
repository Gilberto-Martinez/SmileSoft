from django import forms
from .models import *
from gestion_administrativo.models import Persona

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

class CobroFacturaForm(forms.ModelForm):
    numero_documento = forms.CharField(label="RUC",
                                        widget=forms.TextInput(attrs={
                                                            'class': 'form-control',
                                                            'placeholder': 'Ingrese el RUC del cliente'
                                                            }
                                                    )
                                )
#     dv = forms.IntegerField(label="DV",
#                                 widget=forms.NumberInput(attrs={
#                                                             'class': 'form-control',
#                                                             # 'placeholder': 'Ingrese su nombre'
#                                                             }
#                                                     )
#                                 )
    razon_social = forms.CharField(label="Nombre/Razón social",
                                    widget=forms.TextInput(attrs={
                                                            'class': 'form-control',
                                                            'placeholder': 'Ingrese el nombre del cliente'
                                                            }
                                                    )
                                )
    # domicilio = forms.CharField(label="Domicilio",
    #                                 widget=forms.TextInput(attrs={
    #                                                         'class': 'form-control',
    #                                                         'placeholder': 'Ingrese el domicilio del cliente'
    #                                                         }
    #                                                 )
    #                             ) 

    class Meta:
        model = CobroContado
        fields = [
                    'numero_documento',
                    'razon_social',
        ]

class DatosFacturaForm(forms.ModelForm):
    direccion = forms.CharField(label="Domicilio",
                                    widget=forms.TextInput(attrs={
                                                            'class': 'form-control',
                                                            'placeholder': 'Ingrese el domicilio del cliente'
                                                            }
                                                    )
                                )
    telefono = forms.CharField(label='Teléfono', widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese su numero de telefono'}))
    class Meta:
        model = Persona
        fields = [
                'direccion',
                'telefono'
        ]

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = [
                'numero_documento'
        ]