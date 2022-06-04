from dataclasses import field
from distutils import text_file
from email.headerregistry import Group
from re import U
from django.forms import BooleanField, CheckboxInput, CheckboxSelectMultiple, MultipleHiddenInput, PasswordInput, SelectMultiple, ValidationError, widgets
from tokenize import group
from django import forms
from .models import *
from django.contrib import messages
from django.http import request
from agregar_mas import *
from django.contrib.auth.models import Group, Permission, GroupManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.utils.translation import gettext as _, ngettext

#Import para el Login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm
from django.forms import HiddenInput
from gestion_administrativo.models import Persona

#---------------------------------------------------------------------------------------- FORMULARIO DE INICIO SESION------------------------------------------------------------------------------------#


class UsuarioLoginForm(UserCreationForm):
    # email = forms.EmailField(required=True)
    class Meta:
        model = Usuario
        fields = (
            "usuario",
            # "numero_documento",
            # "email",
            "password1",
        )
        widgets = {
            'numero_documento': HiddenInput(attrs={'required':False}),
               }

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data["password1"])
    #     user.email = self.cleaned_data['email']
    #     if commit:
    #         user.save()
    #     return user



#---------------------------------------------------------------------------------------- FORMULARIOS DEL CRUD DE USUARIO------------------------------------------------------------------------------------#
class UsuarioForm(forms.ModelForm):
    usuario = forms.CharField(max_length=15,
                            #   help_text='<small>✏️ Ejemplo: jperez  ',
                              # error_messages={'required': 'El usuario no puede estar en blanco',
                              #                 'max_length': 'El usuario puede tener hasta 15 caracteres'},

                              widget=forms.TextInput(attrs={'required': True, 'class': 'form-control', 'placeholder': 'Ingrese su usuario'}))
    password1 = forms.CharField(label= "Contraseña",min_length=6 , max_length=25 ,widget=forms.PasswordInput(attrs = {'class': 'form-control', 'placeholder': 'Ingrese su contraseña'}), strip=False)
    password2 = forms.CharField(label="Confirmación de contraseña", min_length=6, max_length=25,help_text='<small> Para verificar, introduzca la misma contraseña anterior.</small>', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirmación de contraseña'}), strip=False)

   #  cargo_Elegir= forms.ModelMultipleChoiceField(
   #     widget = forms.CheckboxSelectMultiple,
   #      queryset = Group.objects.all(),
   #       initial = 0
   #       )

    # estado =forms.ModelMultipleChoiceField(
    #   widget = forms.CheckboxSelectMultiple,
    #    queryset = AbstractBaseUser.objects.all(),
    #     initial = 0

    class Meta:
        proxy = True
      #   ordering = ['-created']
        model = Usuario
       # fields= '__all__'
        fields = [
            'usuario',
            'password1',
            'password2',
            'numero_documento',
            'groups',
            # 'user_permissions',
            'is_active',
            'is_admin',
        ]

        widgets = {
            'groups': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-select2',
                'style': 'width: 20px',
                'multiple': 'multiple'}),

            'password1': forms.PasswordInput(render_value=True,

                                            attrs={
                                                'class': 'from-control',
                                                'placeholder': 'Password ingrese',
                                                'required': 'required'
                                            }
                                            ),

            # 'user_permissions': CheckboxSelectMultiple(attrs={
            #     'class': 'form-select2',

            #     'style': 'width: 50%',
            #     'multiple': 'multiple'
            # }),


        }

        error_messages = {
            'usuario': {
                'max_length': ("Ha Superado la longitud. Ingrese nuevamente el usuario. Por Favor'"),
            },
        }
        
        
    def clean_password2(self):
            # Check that the two password entries match
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")
            if password1 and password2 and password1 != password2:
                raise ValidationError(" ❌ Contraseñas no coinciden")
            return password2
        
    def save(self, commit=True):
            # Save the provided password in hashed format
            usuario = super().save(commit=False)
            usuario.set_password(self.cleaned_data["password1"])
            if commit:
                usuario.save()
            return usuario

class UsuarioUpdateForm(forms.ModelForm):
    usuario = forms.CharField(max_length=15,
                            #   help_text='<small>✏️ Ejemplo: jperez  ',
                              # error_messages={'required': 'El usuario no puede estar en blanco',
                              #                 'max_length': 'El usuario puede tener hasta 15 caracteres'},

                              widget=forms.TextInput(attrs={'required': True, 'class': 'form-control', 'placeholder': 'Ingrese su usuario', 'readonly':True}))
    password1 = forms.CharField(label= "Contraseña",min_length=6 , max_length=25 ,widget=forms.PasswordInput(attrs = {'class': 'form-control', 'placeholder': 'Ingrese su contraseña'}), strip=False)
    password2 = forms.CharField(label="Confirmación de contraseña", min_length=6, max_length=25,help_text='<small> Para verificar, introduzca la misma contraseña anterior.</small>', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirmación de contraseña'}), strip=False)
    numero_documento = forms.CharField(label='N° documento', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Ingrese su documento', 'readonly': 'True'}))
   #  cargo_Elegir= forms.ModelMultipleChoiceField(
   #     widget = forms.CheckboxSelectMultiple,
   #      queryset = Group.objects.all(),
   #       initial = 0
   #       )

    # estado =forms.ModelMultipleChoiceField(
    #   widget = forms.CheckboxSelectMultiple,
    #    queryset = AbstractBaseUser.objects.all(),
    #     initial = 0

    class Meta:
        proxy = True
      #   ordering = ['-created']
        model = Usuario
       # fields= '__all__'
        fields = [
            'usuario',
            'password1',
            'password2',
            'numero_documento',
            'groups',
            # 'user_permissions',
            'is_active',
            'is_admin',
        ]

        widgets = {
            'groups': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-select2',
                'style': 'width: 20px',
                'multiple': 'multiple'}),

            'password1': forms.PasswordInput(render_value=True,

                                            attrs={
                                                'class': 'from-control',
                                                'placeholder': 'Password ingrese',
                                                'required': 'required'
                                            }
                                            ),
            
            # 'numero_documento': CheckboxInput(attrs={
            #                                             'readonly':'True'
            #                                         }),
                                                    
           
            

            # 'user_permissions': CheckboxSelectMultiple(attrs={
            #     'class': 'form-select2',

            #     'style': 'width: 50%',
            #     'multiple': 'multiple'
            # }),

            # 'error_messages' = {
            #     'usuario': {
            #         'max_length': ("Ha Superado la longitud. Ingrese nuevamente el usuario. Por Favor'"),
            #     },
            # }

        }

        
        
    def clean_password2(self):
            # Check that the two password entries match
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")
            if password1 and password2 and password1 != password2:
                raise ValidationError(" ❌ Contraseñas no coinciden")
            return password2
        
    def save(self, commit=True):
            # Save the provided password in hashed format
            usuario = super().save(commit=False)
            usuario.set_password(self.cleaned_data["password1"])
            if commit:
                usuario.save()
            return usuario

# Form que realiza el Autocambio de Contraseña
class PasswordUsuarioForm(forms.Form):
    password1 = forms.CharField(label='Contraseña nueva', min_length=6, max_length=25, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su nueva contraseña...',
            'password1': 'password1',
            'required': 'required',
        }
    ))

    password2 = forms.CharField(label='Contraseña nueva (confirmación)', min_length=6, max_length=25, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese nuevamente la nueva contraseña...',
            'password2': 'password2',
            'required': 'required',
        }
    ))

    def clean_password2(self):
        """ Validación de Contraseña

        Metodo que valida que ambas contraseñas ingresadas sean igual, esto antes de ser encriptadas
        y guardadas en la base dedatos, Retornar la contraseña Válida.

        Excepciones:
        - ValidationError -- cuando las contraseñas no son iguales muestra un mensaje de error
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 != password2:
            raise forms.ValidationError('Contraseñas no coinciden!')
        return password2
    
    #Validaciones, pero no valida
    def password_check(password1):
        SpecialSym = ['$', '@', '#', '%']
        
        if not any(char in SpecialSym for char in password1):
            print('Las contraseñas no cuentan con carateres especiales $@#') 
            raise forms.ValidationError(
                'Las contraseñas no cuentan con carateres especiales $@#')
        val = False
        if val: 
            return val 
        
        if not any(char.isdigit() for char in password1):
          print('La contraseña deberia contar con al menos un dígito numeral')
          raise forms.ValidationError(
        'La contraseña deberia contar con al menos un dígito numeral')
        val = False
    
    def save(self, commit=True):
            # Save the provided password in hashed format
            usuario = super().save(commit=False)
            usuario.set_password(self.cleaned_data["password1"])
            if commit:
                usuario.save()
            return usuario
        

class ConsultaInvitadoForm(forms.ModelForm):
    numero_documento = forms.CharField(
                                        label='N° Cedula de Identidad', 
                                        widget = forms.TextInput (
                                                                    attrs = {
                                                                        'class': 'form-control', 
                                                                        'placeholder': 'Ingrese su número de cedula de identidad',
                                                                    }
                                                                )
                                        )

    class Meta:
        model = Persona
        fields = ['numero_documento',]

class PersonaInvitadaForm(forms.ModelForm):
   nombre= forms.CharField( widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese su nombre'}))
   apellido= forms.CharField( widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese su apellido'}))
   numero_documento= forms.CharField(label='N° documento', widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese su documento',}))
   telefono = forms.CharField(label='Teléfono', widget = forms.TextInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese su numero de telefono'}))
   correo_electronico = forms.EmailField(label='Correo electrónico', widget = forms.EmailInput (attrs = {'class': 'form-control', 'placeholder': 'Ingrese su correo electronico'}))

   class Meta:
         model = Persona
         fields = ['nombre', 
                  'apellido', 
                  'numero_documento', 
                  'telefono',
                  'correo_electronico',
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
