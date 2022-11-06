from django import forms
from gestion_tratamiento.models import TratamientoInsumoAsignado
from .models import *

#---------------------------------------------- FORMULARIOS DEL CRUD DE USUARIO------------------------------------------------------------------------------------#
class InsumoForm(forms.ModelForm):
    nombre_insumo = forms.CharField(label='Nombre del Insumo:', widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese el nombre del insumo'}))
    descripcion_insumo = forms.CharField(label='Descripción del Insumo:', widget = forms.Textarea (attrs = {'class': 'form-control', 'placeholder': 'Breve descripción del insumo'}))
    precio = forms.IntegerField(
                                    label='Costo Unitario:', 
                                   widget = forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': 'Ingrese el precio del insumo:'}))
    fecha_caducidad = forms.DateField(label='Fecha de Caducidad:', widget=forms.DateInput(attrs={'type': 'date'}))
    cantidad_insumo = forms.IntegerField(
                                                   label='Cantidad del Insumo:', 
                                                   widget = forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': 'Ingrese la cantidad del insumo'}))
    # unidad = forms.IntegerField(
    #                                                label='Unidad:', 
    #                                                widget = forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': 'Ingrese la unidad del Insumo'}))
    P = 'Paquete/s'
    C = 'Caja/s'
    L = 'Litro/s'
    UNIDADES = [
            (P, 'Paquete/s'),
            (C, 'Caja/s'),
            (L, 'Litro/s')
            ]
    unidad = forms.ChoiceField(label='Unidad de Medida:', choices=UNIDADES, widget = forms.Select (attrs = {'readonly':'true','class': 'form-control',}))
    MG = 'mg'
    ML = 'ml'
    MM = 'mm'
    A = 'ampollas'
    UDS_UNITARIAS = [
            (MG, 'mg'),
            (ML, 'ml'),
            (ML, 'mm'),
            (A, 'amp/s')
            ]
    ud_unitaria = forms.ChoiceField(label='Ud. de Medida Unitaria:', choices=UDS_UNITARIAS, widget = forms.Select (attrs = {'readonly':'true','class': 'form-control',}))


    unidad_x_paquete = forms.IntegerField(
                                                   label='Ud. Unitaria:', 
                                                   widget = forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': 'Ingrese la ud. unitaria del insumo'}))
    # cantidad_unitaria = forms.IntegerField(
    #                                                label='Cantidad Unitaria:', 
    #                                                widget = forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': 'Cantidad unitaria = cantidad_insumo x unidad_x_paquete'}))
    stock_minimo = forms.IntegerField(
                                                   label='Stock Mínimo:', 
                                                   widget = forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': 'Stock mínimo del insumo'}))
    class Meta:
        model = Insumo
       # fields= '__all__'
        fields = [
            'codigo_insumo',
            'nombre_insumo',
            'descripcion_insumo',
            'precio',
            'fecha_caducidad',
            'cantidad_insumo',
            'unidad',
            'unidad_x_paquete',
            'ud_unitaria',
            #'cantidad_unitaria',
            'stock_minimo',
            #'estado',
        ]

class InsumoUpdateForm(forms.ModelForm):
    nombre_insumo = forms.CharField(label='Nombre del Insumo:', widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese el nombre del insumo'}))
    descripcion_insumo = forms.CharField(label='Descripción del Insumo:', widget = forms.Textarea (attrs = {'class': 'form-control', 'placeholder': 'Breve descripción del insumo'}))
    precio = forms.IntegerField(
                                                   label='Costo Unitario:', 
                                                   widget = forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': 'Ingrese el precio del insumo'}))
    fecha_caducidad = forms.DateField(label='Fecha de Caducidad:', widget=forms.NumberInput(attrs={'type': 'date'}))
    cantidad_insumo = forms.IntegerField(
                                                   label='Cantidad del Insumo:', 
                                                   widget = forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': 'Ingrese la cantidad del insumo'}))
    # unidad = forms.IntegerField(
    #                                                label='Unidad:', 
    #                                                widget = forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': 'Ingrese la unidad del insumo'}))
    P = 'Paquete/s'
    C = 'Caja/s'
    L = 'Litro/s'
    UNIDADES = [
            (P, 'Paquete/s'),
            (C, 'Caja/s'),
            (L, 'Litro/s')
            ]
    unidad = forms.ChoiceField(label='Unidad de Medida:', choices=UNIDADES, widget = forms.Select (attrs = {'readonly':'true','class': 'form-control',}))
    MG = 'mg'
    ML = 'ml'
    MM = 'mm'
    A = 'ampollas'
    UDS_UNITARIAS = [
            (MG, 'mg'),
            (ML, 'ml'),
            (MM, 'mm'),
            (A, 'amp/s')
            ]
    ud_unitaria = forms.ChoiceField(label='Ud. de Medida Unitaria:', choices=UDS_UNITARIAS, widget = forms.Select (attrs = {'readonly':'true','class': 'form-control',}))
    unidad_x_paquete = forms.IntegerField(
                                                   label='Ud. Unitaria:', 
                                                   widget = forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': 'Ingrese la ud. unitaria del insumo'}))
    # cantidad_unitaria = forms.IntegerField(
    #                                                label='Cantidad Unitaria:', 
    #                                                widget = forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': 'Cantidad unitaria = cantidad_insumo x unidad_x_paquete'}))
    stock_minimo = forms.IntegerField(
                                                   label='Stock Mínimo:', 
                                                   widget = forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': 'Stock mínimo del insumo'}))
    class Meta:
        model = Insumo
        #fields= '__all__'
        fields = [
            'codigo_insumo',
            'nombre_insumo',
            'descripcion_insumo',
            'precio',
            'fecha_caducidad',
            'cantidad_insumo',
            'unidad',
            'unidad_x_paquete',
            'ud_unitaria',
            #'cantidad_unitaria',
            'stock_minimo',
            #'estado',
        ]

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

class InsumoAsignadoForm(forms.ModelForm):
    cantidad = forms.IntegerField(
                                    label='Cantidad', 
                                    widget = forms.NumberInput(attrs = {
                                                                        'class': 'form-control', 
                                                                        # 'placeholder': 'Ingrese la cantidad del insumo'
                                                                        }
                                                                )
                                )

    class Meta:
        model = TratamientoInsumoAsignado
        fields = [
            'cantidad',
        ]
