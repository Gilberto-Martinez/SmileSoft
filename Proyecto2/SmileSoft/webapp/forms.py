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
    class Meta:
        model = Usuario
        fields = (
            "usuario",
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
                              widget=forms.TextInput(
                                                    attrs={
                                                            # 'required': False,
                                                            'class': 'form-control',
                                                            'placeholder': 'Ingrese su usuario',
                                                            # 'readonly':True
                                                        }
                                                    )
                            )
    password1 = forms.CharField(label= "Contraseña",min_length=6 , max_length=25 ,widget=forms.PasswordInput(attrs = {'class': 'form-control', 'placeholder': 'Ingrese su contraseña'}), strip=False)
    password2 = forms.CharField(label="Confirmación de contraseña", min_length=6, max_length=25,help_text='<small> Para verificar, introduzca la misma contraseña anterior.</small>', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirmación de contraseña'}), strip=False)

    class Meta:
        proxy = True
        model = Usuario
        fields = [
            'usuario',
            'password1',
            'password2',
            'numero_documento',
            'groups',
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

class UsuarioForm2(forms.ModelForm):
    usuario = forms.CharField(max_length=15,
                              widget=forms.TextInput(
                                                    attrs={
                                                            'required': True,
                                                            'class': 'form-control',
                                                            'placeholder': 'Ingrese su usuario'
                                                        }
                                                    )
                            )
    password1 = forms.CharField(label= "Contraseña",min_length=6 , max_length=25 ,widget=forms.PasswordInput(attrs = {'class': 'form-control', 'placeholder': 'Ingrese su contraseña'}), strip=False)
    password2 = forms.CharField(label="Confirmación de contraseña", min_length=6, max_length=25,help_text='<small> Para verificar, introduzca la misma contraseña anterior.</small>', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirmación de contraseña'}), strip=False)

    class Meta:
        proxy = True
        model = Usuario
        fields = [
            'usuario',
            'password1',
            'password2',
            'numero_documento',
            'groups',
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

#--Modificar usuario
class UsuarioUpdateForm(forms.ModelForm):
    usuario = forms.CharField(max_length=15,
                              widget=forms.TextInput(attrs={
                                                            'required': True,
                                                            'class':'form-control',
                                                            'placeholder': 'Ingrese su usuario',
                                                            'readonly':True
                                                            }
                                                    )
                            )
    numero_documento = forms.CharField(label='N° documento', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Ingrese su documento', 'readonly': 'True'}))

    class Meta:
        proxy = True
        model = Usuario
        fields = [
            'usuario',
            'numero_documento',
            'groups',
            'is_active',
            'is_admin',
        ]
        widgets = {
            'groups': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-select2',
                'style': 'width: 20px',
                'multiple': 'multiple'}),
        }


class UsuarioPassworUpdateForm(forms.ModelForm):
    password1 = forms.CharField(label= "Contraseña",min_length=6 , max_length=25 ,widget=forms.PasswordInput(attrs = {'class': 'form-control', 'placeholder': 'Ingrese su contraseña'}), strip=False)
    password2 = forms.CharField(label="Confirmación de contraseña", min_length=6, max_length=25,help_text='<small> Para verificar, introduzca la misma contraseña anterior.</small>', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirmación de contraseña'}), strip=False)

    class Meta:
        proxy = True
        model = Usuario
        fields = [
            'password1',
            'password2',
        ]

        widgets = {
            'password1': forms.PasswordInput(
                                                render_value=True,
                                                attrs={
                                                        'class': 'from-control',
                                                        'placeholder': 'Password ingrese',
                                                        'required': 'required',
                                                    }
                                            ),
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
        

class ConsultaInvitadoForm(forms.Form):
    numero_documento = forms.CharField(
                                        label='N° Cedula de Identidad', 
                                        widget = forms.TextInput (
                                                                    attrs = {
                                                                        'class': 'form-control', 
                                                                        'placeholder': 'Ingrese su número de cedula de identidad',
                                                                    }
                                                                )
                                        )

    def clean_numero_documento(self):
        data = self.cleaned_data['numero_documento']
        return data

