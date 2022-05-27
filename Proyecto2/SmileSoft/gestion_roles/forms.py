from dataclasses import field, fields
from weakref import proxy
from django import forms
from django.contrib.auth.models import Group, Permission, GroupManager, PermissionsMixin
from webapp.forms import UsuarioForm

from webapp.models import Usuario
from .models import *
from django.utils.translation import gettext_lazy as _


class RolForm(forms.ModelForm):
    name = forms.CharField(label="Nombre del rol", max_length=15,  widget=forms.TextInput(
        attrs={'required': True, 'class': 'form-control', 'placeholder': 'Ingrese nombre del rol'}))

    class Meta:
        proxy = True
        #   ordering = ['-created']
        model = Group
        fields = '__all__'
        # fields = [
        #     'name',
        #   #   'user_permissions',
        # ]
        widgets = {
            'permissions': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-select2',
                'style': 'width: 100px',
                'multiple': 'multiple'
            }), }


class RolUpdateForm(forms.ModelForm):

    name = forms.CharField(label="Nombre del rol", max_length=15,  widget=forms.TextInput(
        attrs={
               'required': True, 'class': 'form-control', 'placeholder': 'Ingrese nombre del rol'}))


    class Meta:
        proxy = True
        #   ordering = ['-created']
        model = Group
        # fields = '__all__'
        fields = [
            'name',
            'permissions',
        ]
        widgets = {
            'permissions': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-select2',
                'style': 'width: 100px',
                'multiple': 'multiple',
                'readonly': True
            }), }
        

 