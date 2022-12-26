from django.forms import *
from django import forms
from gestion_cobros.models import Factura


class ReporteFacturaForm(Form):
    date_range = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))

# class FiltroFechas(forms.ModelForm):

#     class Meta:
#         model = Factura
#         fields = ['fecha', 'fecha_fin']
#         widgets = {
#              'fecha': forms.DateInput(format=('%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y',), attrs={'class': 'form-control bs-datepicker', 'placeholder': 'Seleccione la fecha de inicio'}),
#              'fecha_fin': forms.DateInput(format=('%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y',), attrs={'class': 'form-control bs-datepicker', 'placeholder': 'Seleccione la fecha fin'})
#         }