from django.db import models
from gestion_administrativo.models import *

# Create your models here.

class Tratamiento(models.Model):
    codigo_tratamiento= models.AutoField(primary_key=True, verbose_name='Código de tratamiento (*):')
    nombre_tratamiento= models.CharField(max_length=100, verbose_name='nombre (*):')
    descripcion_tratamiento= models.TextField(max_length=500, verbose_name='Descripción (*):',null= True,)
    precio=models.IntegerField(verbose_name='precio (*):')
    # especialista = models.ForeignKey(EspecialistaSalud)
    
    class Meta:
        verbose_name = ("tratamiento")
        verbose_name_plural = ("tratamientos")
        db_table = 'Tratamiento'
        ordering = ['nombre_tratamiento']

    def __str__(self):
        return self.nombre_tratamiento

""" class Categoria(models.Model):
    codigo_categoria= models.AutoField(primary_key=True, verbose_name='codigo')
    detalle_tratamiento= models.CharField(max_length=40, verbose_name='detalle')
    precio=models.IntegerField()
    codigo_tratamiento = models.ForeignKey(Tratamiento, null=False, blank=False, on_delete=models.CASCADE)

    
    class Meta:
        verbose_name = ("Categoria")
        verbose_name_plural = ("Categorias")
        db_table = 'Categoria'

    def __str__(self):
        return self.detalle_tratamiento
 """