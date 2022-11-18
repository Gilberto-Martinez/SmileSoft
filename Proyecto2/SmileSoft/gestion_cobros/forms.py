from django import forms
from .models import *
from gestion_administrativo.models import Persona, Empresa

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

class FacturaForm(forms.ModelForm):
    numero_documento = forms.CharField(label="RUC",
                                        widget=forms.TextInput(attrs={
                                                            'class': 'form-control',
                                                            'placeholder': 'Ingrese el RUC del cliente'
                                                            }
                                                    )
                                )
    dv = forms.IntegerField(label="DV",
                                widget=forms.NumberInput(attrs={
                                                            'class': 'form-control',
                                                            # 'placeholder': 'Ingrese su nombre'
                                                            }
                                                    )
                                )
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

class DomicilioForm(forms.ModelForm):
    direccion = forms.CharField(label="Domicilio",
                                    widget=forms.TextInput(attrs={
                                                            'class': 'form-control',
                                                            'placeholder': 'Ingrese el domicilio del cliente'
                                                            }
                                                    )
                                ) 
    class Meta:
        model = Persona
        fields = [
                'direccion'
        ]



class EmpresaForm(forms.ModelForm):
        # nombre_empresa = models.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
        # direccion=forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}))


        class Meta:
                model = Empresa
                fields = [
                        'nombre_empresa',
                        'direccion',
                        'telefono',
                        'correo_electronico',
                        'ruc',
                        'timbrado',
                        'f_inicio_vigencia',
                        'f_fin_vigencia',
                        
                ]


