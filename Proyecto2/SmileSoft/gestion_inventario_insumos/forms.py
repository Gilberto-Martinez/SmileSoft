from django import forms
from gestion_tratamiento.models import TratamientoInsumoAsignado
from .models import *

#---------------------------------------------- FORMULARIOS DEL CRUD DE USUARIO------------------------------------------------------------------------------------#
class InsumoForm(forms.ModelForm):
    nombre_insumo = forms.CharField(label='Nombre del Insumo:', widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese el nombre del insumo'}))
    descripcion_insumo = forms.CharField(label='Descripción del Insumo:', widget = forms.Textarea (attrs = {'class': 'form-control', 'placeholder': 'Breve descripción del insumo'}))
    precio = forms.IntegerField(
                                    label='Costo:', 
                                   widget = forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': 'Ingrese el precio del insumo:'}))
    fecha_caducidad = forms.DateField(label='Fecha de caducidad', widget=forms.DateInput(attrs={'type': 'date'}))
    cantidad_insumo = forms.IntegerField(
                                                   label='Cantidad del Insumo:', 
                                                   widget = forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': 'Ingrese la cantidad del insumo'}))
    # unidad = forms.IntegerField(
    #                                                label='Unidad:', 
    #                                                widget = forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': 'Ingrese la unidad del Insumo'}))
    P = 'Paquetes'
    C = 'Cajas'
    L = 'Litros'
    UNIDADES = [
            (P, 'Paquetes'),
            (C, 'Cajas'),
            (L, 'Litros')
            ]
    unidad = forms.ChoiceField(label='Unidad:', choices=UNIDADES, widget = forms.Select (attrs = {'readonly':'true','class': 'form-control',}))
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
            #'estado',
        ]

class InsumoUpdateForm(forms.ModelForm):
    nombre_insumo = forms.CharField(label='Nombre del Insumo:', widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese el nombre del insumo'}))
    descripcion_insumo = forms.CharField(label='Descripción del Insumo:', widget = forms.Textarea (attrs = {'class': 'form-control', 'placeholder': 'Breve descripción del insumo'}))
    precio = forms.IntegerField(
                                                   label='Costo:', 
                                                   widget = forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': 'Ingrese el precio del insumo'}))
    fecha_caducidad = forms.DateField(label='Fecha de caducidad', widget=forms.NumberInput(attrs={'type': 'date'}))
    cantidad_insumo = forms.IntegerField(
                                                   label='Cantidad del Insumo:', 
                                                   widget = forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': 'Ingrese la cantidad del insumo'}))
    # unidad = forms.IntegerField(
    #                                                label='Unidad:', 
    #                                                widget = forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': 'Ingrese la unidad del insumo'}))
    P = 'Paquetes'
    C = 'Cajas'
    L = 'Litros'
    UNIDADES = [
            (P, 'Paquetes'),
            (C, 'Cajas'),
            (L, 'Litros')
            ]
    unidad = forms.ChoiceField(label='Unidad:', choices=UNIDADES, widget = forms.Select (attrs = {'readonly':'true','class': 'form-control',}))
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
        #     'unidad',
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

class InsumoAsignadoForm(forms.ModelForm):
    cantidad = forms.IntegerField(
                                    label='Cantidad', 
                                    widget = forms.NumberInput(attrs = {
                                                                        'class': 'form-control', 
                                                                        'placeholder': 'Ingrese la cantidad del insumo'
                                                                        }
                                                                )
                                )

    class Meta:
        model = TratamientoInsumoAsignado
        fields = [
            'cantidad',
        ]
