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

# class RazonSocialForm(forms.ModelForm):
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

#     class Meta:
#         model = CobroContado
#         fields = [
#                     'numero_documento',
#                     'razon_social',
#         ]

class CobroFacturaForm(forms.ModelForm):
    numero_documento = forms.CharField(label="RUC",
                                        widget=forms.TextInput(attrs={
                                                            'class': 'form-control',
                                                            'placeholder': 'Ingrese el RUC del cliente'
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
    numero_documento = forms.CharField(label="RUC",
                                        widget=forms.TextInput(attrs={
                                                            'class': 'form-control',
                                                            'placeholder': 'Ingrese el RUC del cliente'
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
    direccion = forms.CharField(label="Domicilio",
                                    widget=forms.TextInput(attrs={
                                                            'class': 'form-control',
                                                            'placeholder': 'Ingrese el domicilio del cliente'
                                                            }
                                                    )
                                )
    telefono = forms.CharField(label='Teléfono', widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese su numero de telefono'}))
    CO = 'Contado'
    CR = 'Credito'
    CONDICIONES = ((CO, 'Contado'), (CR, 'Credito'))
    condicion_venta = forms.ChoiceField(label='Condicón de venta',choices=CONDICIONES, widget = forms.Select (attrs = {'class': 'form-control',}))
    fecha = forms.CharField( widget=forms.TextInput(attrs={'class': 'form-control', 'readonly':True}))
    class Meta:
        model = Factura
        fields = [
                'numero_documento',
                'razon_social',
                'direccion',
                'telefono',
                'condicion_venta',
                'fecha',
        ]


class FacturaUpdateForm(forms.ModelForm):
    nro_factura = forms.CharField(label="Número de factura",
                                        widget=forms.TextInput(attrs={
                                                            'class': 'form-control',
                                                            'readonly':True,
                                                            }
                                                    )
                                )

    numero_documento = forms.CharField(label="RUC",
                                        widget=forms.TextInput(attrs={
                                                            'class': 'form-control',
                                                            'readonly':True,
                                                            }
                                                    )
                                )
    razon_social = forms.CharField(label="Nombre/Razón social",
                                    widget=forms.TextInput(attrs={
                                                            'class': 'form-control',
                                                            'readonly':True,
                                                            }
                                                    )
                                )
    direccion = forms.CharField(label="Domicilio",
                                    widget=forms.TextInput(attrs={
                                                            'class': 'form-control',
                                                            'readonly':True,
                                                            }
                                                    )
                                )
                                                        
    telefono = forms.CharField(label='Teléfono', widget = forms.TextInput (attrs = {
                                                                                'class': 'form-control',
                                                                                'readonly':True,
                                                                                }
                                                                        )
                                )

    condicion_venta = forms.CharField(label='Condición de venta', widget = forms.TextInput (attrs = {
                                                                                'class': 'form-control',
                                                                                'readonly':True,
                                                                                }
                                                                        )
                                )
    total_pagar = forms.IntegerField(label='Total a pagar', widget = forms.NumberInput (attrs = {
                                                                                'class': 'form-control',
                                                                                'readonly':True,
                                                                                }
                                                                        )
                                )
    E = 'Emitido'
    A = 'Anulado'
    ESTADOS = ((E, 'Emitido'), (A, 'Anulado'))
    estado = forms.ChoiceField(choices=ESTADOS, widget = forms.Select (attrs = {'class': 'form-control',}))
    
    class Meta:
        model = Factura
        fields = [
                'nro_factura',
                'numero_documento',
                'razon_social',
                'direccion',
                'telefono',
                'condicion_venta',
                'total_pagar',
                'estado',
        ]


class FacturaReadOnlyForm(forms.ModelForm):
    nro_factura = forms.CharField(label="Número de factura",
                                        widget=forms.TextInput(attrs={
                                                            'class': 'form-control',
                                                            'readonly':True,
                                                            }
                                                    )
                                )

    numero_documento = forms.CharField(label="RUC",
                                        widget=forms.TextInput(attrs={
                                                            'class': 'form-control',
                                                            'readonly':True,
                                                            }
                                                    )
                                )
    razon_social = forms.CharField(label="Nombre/Razón social",
                                    widget=forms.TextInput(attrs={
                                                            'class': 'form-control',
                                                            'readonly':True,
                                                            }
                                                    )
                                )
    direccion = forms.CharField(label="Domicilio",
                                    widget=forms.TextInput(attrs={
                                                            'class': 'form-control',
                                                            'readonly':True,
                                                            }
                                                    )
                                )
                                                        
    telefono = forms.CharField(label='Teléfono', widget = forms.TextInput (attrs = {
                                                                                'class': 'form-control',
                                                                                'readonly':True,
                                                                                }
                                                                        )
                                )

    condicion_venta = forms.CharField(label='Condición de venta', widget = forms.TextInput (attrs = {
                                                                                'class': 'form-control',
                                                                                'readonly':True,
                                                                                }
                                                                        )
                                )
    total_pagar = forms.IntegerField(label='Total a pagar', widget = forms.NumberInput (attrs = {
                                                                                'class': 'form-control',
                                                                                'readonly':True,
                                                                                }
                                                                        )
                                )
    estado = forms.CharField( widget = forms.TextInput (attrs = {'class': 'form-control', 'readonly':True}))
    
    class Meta:
        model = Factura
        fields = [
                'nro_factura',
                'numero_documento',
                'razon_social',
                'direccion',
                'telefono',
                'condicion_venta',
                'total_pagar',
                'estado',
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

class CajaForm(forms.ModelForm):
    # id_cajero = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
#     fecha_apertura = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
#     hora_apertura = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    # fecha_cierre = models.DateField()
    # hora_cierre = models.TimeField()
#     saldo_anterior = forms.IntegerField( widget=forms.NumberInput(attrs={'class':'form-control'}))
    monto_apertura = forms.IntegerField( widget=forms.NumberInput(attrs={'class':'form-control'}))
    # monto_cierre = models.BigIntegerField()

    class Meta:
        model = Caja
        fields = [
                # 'id_cajero',
                # 'fecha_apertura',
                # 'hora_apertura',
                # 'fecha_cierre',
                # 'hora_cierre',
                'saldo_anterior',
                'monto_apertura',
                # 'monto_cierre',
        ]

# class GastoForm(forms.ModelForm):
#     class Meta:
#         model = Gasto
#         fields = [
#                 'monto_total',
#         ]


class ComprobanteGastoForm(forms.ModelForm):
    numero_comprobante = forms.CharField(label='Número de comprobante', widget=forms.TextInput(attrs={'class':'form-control',}))
    CO = 'Contado'
    CR = 'Credito'
    CONDICIONES = ((CO, 'Contado'), (CR, 'Credito'))
    condicion_venta = forms.ChoiceField(label='Condición de venta', choices=CONDICIONES, widget=forms.Select(attrs={'class': 'form-control',}))
    class Meta:
        model = ComprobanteGasto
        fields = [
                'numero_comprobante', 
                'condicion_venta',
        ]


class DetalleComprobanteForm(forms.ModelForm):
    class Meta:
        model = DetalleComprobante
        fields = [
                'descripcion',
                'cantidad',
                'precio_unitario',
                'comprobante',
        ]


# class DetalleGastoForm(forms.ModelForm):
#     class Meta:
#         model = DetalleGasto
#         fields = [
#                 'descripcion',
#                 'precio_unitario',
#         ]