from django.db import models
from gestion_administrativo.models import *
from gestion_inventario_insumos.models import *

# Create your models here.

class Insumo(models.Model):
    codigo_insumo= models.AutoField(primary_key=True, verbose_name='Código de tratamiento (*):')
    nombre_insumo= models.CharField(max_length=100, verbose_name='nombre (*):')
    descripción_insumo= models.TextField(max_length=500, verbose_name='Descripción ():')
    precio=models.IntegerField(verbose_name='precio (*):')
    fecha_caducidad=models.DateField(verbose_name='Fecha de caducidad del insumo')

        
    # especialista = models.ForeignKey(EspecialistaSalud)
    LOAN_STATUS = (
        ('Disponible', 'Disponible'),
        ('Intermedio', 'Intermedio'),
        ('En Falta', 'En Falta'),
    )
    estado = models.CharField(max_length=15, choices=LOAN_STATUS, blank=True, default='Disponible', help_text='Disponibilidad del Insumo')
    
    class Meta:
        verbose_name = ("insumo")
        verbose_name_plural = ("insumos")
        db_table = 'Insumo'
        ordering = ['nombre_insumo']

    def __str__(self):
        return self.nombre_insumo

