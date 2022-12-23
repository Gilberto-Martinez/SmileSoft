from django.forms import *
from django import forms
from gestion_cobros.models import Factura


class ReporteFacturaForm(Form):
    date_range = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))
