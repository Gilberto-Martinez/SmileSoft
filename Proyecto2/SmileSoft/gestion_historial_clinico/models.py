from django.db import models
from django.db.models.deletion import PROTECT
from django.db.models.fields.related import ForeignKey
from django.template.defaultfilters import default
#from SmileSoft.gestion_administrativo.models import Persona
#from agregar_mas.models import *
#from gestion_tratamiento.models import Tratamiento

# Create your models here.
'''
class AntecedenteClinico(models.Model):
    id_antecedente = models.AutoField(primary_key=True)
    enfermedad_base = models.CharField(max_length=60, verbose_name='Enfermedad de base (*)')
    alergia = models.CharField(max_length=60,  verbose_name='Alergia (*)')
    tolerancia_anestecia = models.BooleanField(verbose_name='Tolerancia a la anestecia', default=False)
    frecuencia_higiene_bucal = models.CharField(max_length=60,  verbose_name='Frecuencia de higiene bucal (*)')
    medicamento = models.CharField(max_length=60,  verbose_name='Medicamento/s (*)')
    cirugias = models.BooleanField(default=False, verbose_name='Cirugías (*)')
    caries = models.BooleanField(default=False, verbose_name='Caries (*)')
    afeccion_cronica_familiar = models.CharField(max_length=500,  verbose_name='Afección crónica familiar (*)')
    afecciones_graves = models.CharField(max_length=500,  verbose_name='Afecciones graves (*)')
    grupo_sanguineo = models.CharField(max_length=100,  verbose_name='Grupo sanguíneo (*)')

    class Meta:
        # ordering = ['nombre']
        verbose_name_plural = 'Antecedentes Clinicos'
        db_table = 'AntecedenteClinico'

    def __str__(self):
        return str(self.id_antecedente)
'''
class HistorialClinico(models.Model):
    numero_ficha = models.AutoField(primary_key=True, verbose_name='Número de Ficha')
    #id_antecedente = models.ForeignKey(AntecedenteClinico, on_delete=models.PROTECT)    
    
    class Meta:
        verbose_name = 'Historial Clinico'
        verbose_name_plural = 'Historiales Clinicos'
        db_table = 'HistorialClinico'

    def __str__(self):
        return str(self.numero_ficha)

""" class TratamientoRealizado(models.Model):
    id_tratamiento_realizado = models.AutoField(primary_key=True, verbose_name='Número de tratamiento realizado')
    codigo_tratamiento = models.ForeignKey(
                                            Tratamiento, 
                                            null=False, 
                                            blank=False, 
                                            on_delete=models.PROTECT,
                                            verbose_name='Código de tratamiento'
                                        )
    numero_documento = models.ForeignKey(
                                            Paciente, 
                                            null=False, 
                                            blank=False, 
                                            on_delete=models.PROTECT,
                                            verbose_name='Número de documento'
                                        )
    numero_ficha = models.ForeignKey(HistorialClinico,verbose_name='Número de ficha',on_delete=models.PROTECT)
    
    class Meta:
        verbose_name = 'Tratamientos Realizados'
        db_table = 'TratamientoRealizado'

    def __str__(self):
        return str(self.numero_ficha) """