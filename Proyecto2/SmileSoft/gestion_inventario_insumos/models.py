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
    precio=models.IntegerField(verbose_name='Costo Unitario (*):')
    fecha_caducidad = models.DateField(verbose_name='Fecha de nacimiento')
    cantidad_insumo = models.IntegerField(default=0, verbose_name= 'Cantidad (*)') #Cantidad_insumo =  5  Paquetes/Cajas/Litros --> se agrega por teclado
    #unidad = models.IntegerField(default=0, verbose_name= 'Unidad (*)')
    unidad_x_paquete = models.IntegerField(default=0, verbose_name= 'Unidad por pcl (*)')#donde pcl es unidad por paquete caja o litro # unidad_x_paquete = 12  --> se agrega por teclado
    cantidad_unitaria = models.IntegerField(default=0, verbose_name= 'Cantidad unitaria (*)') #cantidad_unitaria = 5 x 12 = 60    unidad --> no se agrega por teclado
    stock_minimo = models.IntegerField(default=0, verbose_name= 'Stock mínimo (*)') #stock_minimo = 12 --> se agrega por teclado
   # existencia = si cantidad_unitaria < stock_minimo entoces "en falta" sino "disponible"
    P = 'Paquete/s'
    C = 'Caja/s'
    L = 'Litro/s'
    UNIDADES = ((P, 'Paquete/s'), (C, 'Caja/s'), (L, 'Litro/s'))
    unidad = models.CharField(max_length=12, choices=UNIDADES, verbose_name='Unidad de medida')
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