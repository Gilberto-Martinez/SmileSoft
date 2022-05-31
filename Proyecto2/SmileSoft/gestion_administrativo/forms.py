#from _typeshed import Self
from re import VERBOSE
from django import forms
from django.contrib import messages
from .models import *
from webapp.models import *
from django.forms import HiddenInput
from django.forms.models import InlineForeignKeyField
# from betterforms.multiform import MultiModelForm
#from django.core.mail import EmailMessage
from gestion_administrativo.models import Paciente

class PersonaForm(forms.ModelForm):
   nombre= forms.CharField( widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese su nombre'}))
   apellido= forms.CharField( widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese su apellido'}))
   numero_documento= forms.CharField(label='N° documento', widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese su documento',}))
   direccion = forms.CharField(label='Dirección', widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese su dirección'}))
   telefono = forms.CharField(label='Teléfono', widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese su numero de telefono'}))
   correo_electronico = forms.EmailField(label='Correo electrónico', widget = forms.EmailInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese su correo electronico'}))
   #fecha_nacimiento = forms.DateField( widget = forms.DateInput (attrs = {'class': 'form-control'}))
   F = 'Femenino'
   M = 'Masculino'
   SEXOS = [
            (F, 'Femenino'),
            (M, 'Masculino')
   ]
   sexo = forms.ChoiceField(choices=SEXOS, widget = forms.Select (attrs = {'class': 'form-control',}))
   # fecha_nacimiento = forms.DateField(label='Fecha de nacimiento', widget=forms.NumberInput(attrs={'type': 'date'}))
   fecha_nacimiento = forms.DateField(label='Fecha de nacimiento', widget=forms.DateInput(attrs={'type': 'date'}))
   
                                      
   class Meta:
        model = Persona
        fields = ['nombre', 
                  'apellido', 
                  'numero_documento', 
                  'direccion',
                  'telefono',
                  'correo_electronico',
                  'fecha_nacimiento',
                  'sexo',
                ]

   def clean_numero_documento(self):
      numero_documento= self.cleaned_data["numero_documento"]
      if Persona.objects.filter(numero_documento=numero_documento).exists():
         print ("Ya existe el numero de cedula ingresado")
         #messages.error(request, 'Ya existe el numero de cedula ingresado')
            # self.error_cedula()
      return numero_documento

   def get_numero_documento(self):
      return self.numero_documento
    
    # def error_cedula(self):
    #     respuesta =request.HttpRequest()
    #     messages.error(respuesta, "Ya existe el numero de cedula ingresado" )      

class FuncionarioForm(forms.ModelForm):
   # cargos= forms.ModelMultipleChoiceField(queryset=Cargo.objects.all(),widget = forms.SelectMultiple (attrs = {'class': 'form-control',}))
   # cargo = forms.ComboField(fields='cargos')
   # numero_documento= forms.CharField(label='Número de documento', widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese su documento',}))
   class Meta:
      model = Funcionario
      fields = [
               # 'numero_documento',
               'cargos',
                ]
      widgets = {
          'cargos': forms.CheckboxSelectMultiple(attrs={
              'class': 'form-select2',
              'style': 'width: 30px',
              'multiple': 'multiple'}),
               #  'numero_documento': HiddenInput(attrs={'required': False})
            'es_funcionario': HiddenInput(attrs={'required':False}),
            'es_paciente': HiddenInput(attrs={'required':False}),
            'es_personal_salud': HiddenInput(attrs={'required':False}),
               }
      # InlineForeignKeyField(Cargo)
            


class PersonaUpdateForm(forms.ModelForm):
   nombre= forms.CharField( widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese su nombre'}))
   apellido= forms.CharField( widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese su apellido'}))
   numero_documento= forms.CharField(label='N° documento', widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese su documento','readonly':'True'}))
   direccion = forms.CharField(label='Dirección', widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese su dirección'}))
   telefono = forms.CharField(label='Teléfono', widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese su numero de telefono'}))
   correo_electronico = forms.EmailField(label='Correo electrónico', widget = forms.EmailInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese su correo electronico'}))
   #fecha_nacimiento = forms.DateField( widget = forms.DateInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese su fecha de nacimiento'}))
   F = 'Femenino'
   M = 'Masculino'
   SEXOS = [
            (F, 'Femenino'),
            (M, 'Masculino')
   ]
   sexo = forms.ChoiceField(choices=SEXOS, widget = forms.Select (attrs = {'class': 'form-control',}))
   fecha_nacimiento = forms.DateField(label='Fecha de nacimiento', widget=forms.NumberInput(attrs={'type': 'date'}))

   class Meta:
        model = Persona
        fields = ['nombre', 
                  'apellido', 
                  'numero_documento', 
                  'direccion',
                  'telefono',
                  'correo_electronico',
                  'fecha_nacimiento',
                  'sexo',
                ]

   def clean_numero_documento(self):
      numero_documento= self.cleaned_data["numero_documento"]
      if Persona.objects.filter(numero_documento=numero_documento).exists():
         print ("Ya existe el numero de cedula ingresado")
         #messages.error(request, 'Ya existe el numero de cedula ingresado')
            # self.error_cedula()
      return numero_documento

   def get_numero_documento(self):
      return self.numero_documento


class EspecialistaSaludForm(forms.ModelForm):
   class Meta:
      model = EspecialistaSalud
      fields = [
                 'trabajos_realizados',
               ]
      widgets = {
         # 'trabajos_realizados': forms.CheckboxSelectMultiple(attrs={
         #      'class': 'form-select2',
         #      'style': 'width: 20px',
         #      'multiple': 'multiple'}),
         'trabajos_realizados':HiddenInput(attrs={'required':False}),
               }

class ProveedorForm(forms.ModelForm):
   ruc= forms.CharField( widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese el ruc del proveedor'}))
   nombre= forms.CharField( widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese el nombre del proveedor'}))
   direccion= forms.CharField( widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese la dirección del proveedor'}))
   telefono= forms.CharField( widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese el telefono del proveedor'}))
   correo_electronico= forms.CharField( widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese el correo electrónico del proveedor'}))
   class Meta:
      model = Proveedor
      fields = [
                 'ruc',
                 'nombre',
                 'direccion',
                 'telefono',
                 'correo_electronico',
                 #'producto',
               ]
      # widgets = {
      #    'producto': forms.CheckboxSelectMultiple(attrs={
      #         'class': 'form-select2',
      #         'style': 'width: 20px',
      #         'multiple': 'multiple'}),
      #          }

class ProveedorUpdateForm(forms.ModelForm):
   ruc= forms.CharField( widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese el ruc del proveedor', 'readonly':True}))
   nombre= forms.CharField( widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese el nombre del proveedor'}))
   direccion= forms.CharField( widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese la dirección del proveedor'}))
   telefono= forms.CharField( widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese el telefono del proveedor'}))
   correo_electronico= forms.CharField( widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese el correo electrónico del proveedor'}))
   class Meta:
      model = Proveedor
      fields = [
                 'ruc',
                 'nombre',
                 'direccion',
                 'telefono',
                 'correo_electronico',
                 #'producto',
               ]
      # widgets = {
      #    'producto': forms.CheckboxSelectMultiple(attrs={
      #         'class': 'form-select2',
      #         'style': 'width: 20px',
      #         'multiple': 'multiple'}),
      #          }


class PacienteForm(forms.ModelForm):
   # NN = 'No especificado'
   # S = 'SI'
   # N = 'NO'
   # OPCIONES =[
   #             (NN, 'No especificado'),
   #             (S, 'SI'),
   #             (N, 'NO')
   # ]
   # tolerancia_anestecia = forms.ChoiceField(
   #                                           label='¿Tolera el uso de anestecia?', 
   #                                           choices=OPCIONES, 
   #                                           widget = forms.Select (attrs = {'class': 'form-control',}))
   frecuencia_higiene_bucal = forms.IntegerField(
                                                   label='Frecuencia de higiene bucal', 
                                                   widget = forms.NumberInput(attrs = {'class': 'form-control', 'placeholder': '¿Cuantas veces al día realiza higiene bucal?'}))
   medicamento = forms.CharField(label='Medicamentos', widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Si consume medicamentos especifique cuales son'}))
   # cirugias = forms.ChoiceField(label='¿Se ha sometido a alguna cirugia?', choices=OPCIONES, widget = forms.Select (attrs = {'class': 'form-control',}))
   # caries = forms.ChoiceField(label='¿Tiene caries?', choices=OPCIONES, widget = forms.Select (attrs = {'class': 'form-control',}))
   NN = 'No especificado'
   AP = 'A RH+'
   AN = 'A Rh-'
   BP = 'B RH+'
   BN = 'B RH-'
   OP = '0 RH+'
   ON = '0 RH-'
   ABP = 'AB RH+'
   ABN = 'AB RH-'
   GRUPOS = [
            (NN, 'No especificado'),
            (AP, 'A RH+'),
            (AN, 'A Rh-'),
            (BP, 'B RH+'),
            (BN, 'B RH-'),
            (OP, '0 RH+'),
            (ON, '0 RH-'),
            (ABP, 'AB RH+'),
            (ABN, 'AB RH-'),
    ]
   grupo_sanguineo = forms.ChoiceField(choices=GRUPOS, widget = forms.Select (attrs = {'class': 'form-control',}))
   enfermedad_base = forms.CharField(label='Enfermedades de base', widget = forms.Textarea (attrs = {'class': 'form-control', 'placeholder': 'Si tiene enfermedades de base especidfique cuales son'}))
   alergia = forms.CharField( widget = forms.Textarea (attrs = {'class': 'form-control', 'placeholder': 'Si tiene alergias especifique cuales son'}))
   afeccion_cronica_familiar = forms.CharField(label='Afección crónica familiar', widget = forms.Textarea (attrs = {'class': 'form-control', 'placeholder': 'Ingrese las afecciones cronicas familiares'}))
   class Meta:
         model = Paciente
         fields = [
                  'tolerancia_anestecia',
                  'frecuencia_higiene_bucal',
                  'medicamento',
                  'cirugias',
                  'caries',
                  'grupo_sanguineo',
                  'enfermedad_base',
                  'alergia',
                  'afeccion_cronica_familiar',
                ]
         # widgets = {
         #        'numero_documento': HiddenInput(attrs={'required': False})
         #       }


class CargoForm(forms.ModelForm):
   nombre = forms.CharField(
                           label='Nombre del cargo', 
                           widget = forms.TextInput (
                                                   attrs = {
                                                      'class': 'form-control', 
                                                      'placeholder': 'Ingrese el nombre del cargo'
                                                      }
                                                   )
                           )
   salario = forms.IntegerField(
                           label='Salario', 
                           widget = forms.NumberInput (
                                                   attrs = {
                                                      'class': 'form-control', 
                                                      'placeholder': 'Ingrese el salario'
                                                      }
                                                   )
                           )
   class Meta:
      model = Cargo
      fields = [
                 'nombre',
                 'salario',
               ]

##############################################################################################
#PARA ASIGNAR TRATAMIENTO


from django import forms


from webapp.models import Usuario
from .models import *
from django.utils.translation import gettext_lazy as _


# class AsignarTratamientoForm(forms.ModelForm):
    
#     class Meta:
#         #proxy = True
#         #   ordering = ['-created']
#         model = TratamientoRealizado
#         fields = '__all__'
#         # fields = [
#         #     'name',
#         #     'user_permissions',
#         # ]
#         widgets = {
#             'nombre_tratamiento': forms.CheckboxSelectMultiple(attrs={
#                 'class': 'form-select2',
#                 'style': 'width: 100px',
#                 'multiple': 'multiple'
#             }), }

class PacienteAsignadoForm(forms.ModelForm):
   # cargos= forms.MultiValueField(fields= 'cargos' ,widget = forms.TextInput (attrs = {'class': 'form-control',}))
   # cargo = forms.ComboField(fields='cargos')
   # numero_documento= forms.CharField(label='Número de documento', widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese su documento',}))
   class Meta:
      model = PacienteTratamientoAsignado
      fields = [
               'paciente',
               'nombre_tratamiento',
                ]
      widgets = {
          'nombre_tratamiento': forms.CheckboxSelectMultiple(attrs={
              'class': 'form-select2',
              'style': 'width: 30px',
              'multiple': 'multiple'}),
               #  'numero_documento': HiddenInput(attrs={'required': False})

               }
 

