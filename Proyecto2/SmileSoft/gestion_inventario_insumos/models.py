from pyexpat import model

from django.db import models
from gestion_administrativo.models import *
from gestion_inventario_insumos.models import *

# Create your models here.


#clase planilla
#que tenga una lista del tipo insumo

# class Inventario(models.Model):
#     insumos=[]

#     def cargar_insumos(self,insumo):
#         self.insumos.append(insumo)

#     def contar_insumos(self):
#         cantidad = 0
#         for insumo in self.insumos:
#             cantidad = cantidad + 1
#         return cantidad
# de 1 a muchos

class Insumo(models.Model):
    codigo_insumo= models.AutoField(primary_key=True, verbose_name='Código de tratamiento (*):')
    nombre_insumo= models.CharField(max_length=100, verbose_name='Nombre (*):')
    descripcion_insumo= models.TextField(max_length=500, verbose_name='Descripción (*):')
    precio=models.IntegerField(verbose_name='Costo (*):')
    fecha_caducidad = models.DateField(verbose_name='Fecha de nacimiento')
    cantidad_insumo = models.IntegerField(default=0, verbose_name= 'Cantidad (*)')
    #unidad = models.IntegerField(default=0, verbose_name= 'Unidad (*)')
    P = 'Paquetes'
    C = 'Cajas'
    L = 'Litros'
    UNIDADES = ((P, 'Paquetes'), (C, 'Cajas'), (L, 'Litros'))
    unidad = models.CharField(max_length=12, choices=UNIDADES, verbose_name='Unidad')
    #id_inventario = models.ForeignKey(inventario)

        
  
    # LOAN_STATUS = (
    #     ('Disponible', 'Disponible'),
    #     ('Intermedio', 'Intermedio'),
    #     ('En Falta', 'En Falta'),
    # )
    # estado = models.CharField(max_length=15, choices=LOAN_STATUS, blank=True, default='Disponible', help_text='Disponibilidad del Insumo')
    
    class Meta:
        verbose_name = ("insumo")
        verbose_name_plural = ("insumos")
        db_table = 'Insumo'
        ordering = ['nombre_insumo']

    def __str__(self):
        return self.nombre_insumo

#insumo con caducidad