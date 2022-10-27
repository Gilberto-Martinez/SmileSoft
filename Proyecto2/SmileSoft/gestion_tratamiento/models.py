from django.db import models
from gestion_inventario_insumos.models import Insumo

# Create your models here.

class Tratamiento(models.Model):
    codigo_tratamiento= models.AutoField(primary_key=True, verbose_name='Código de tratamiento (*):')
    nombre_tratamiento= models.CharField(max_length=100, verbose_name='nombre (*):')
    descripcion_tratamiento= models.TextField(max_length=500, verbose_name='Descripción (*):',null= True,)
    precio=models.IntegerField(verbose_name='precio (*):')
    insumos = models.ManyToManyField(
                                             Insumo, 
                                             through='TratamientoInsumoAsignado',
                                             related_name='tratamiento_set',
                                             blank=True, 
                                             )

    class Meta:
        verbose_name = ("tratamiento")
        verbose_name_plural = ("tratamientos")
        ordering = ["nombre_tratamiento"]
        db_table = 'Tratamiento'

    def __str__(self):
        return str(self.nombre_tratamiento)

    def get_id(self):
        return str(self.codigo_tratamiento)

    def get_codigo_tratamiento(self):
        return str(self.codigo_tratamiento)
   

#Modelo CATEGORIA

class TratamientoCategoria(models.Model):
    id_categoria_tratamiento = models.AutoField(primary_key=True,)
    tratamiento= models.ForeignKey(Tratamiento,on_delete=models.CASCADE, 
                                                    blank=True, 
                                                    null=True,)
    SIMPLE = 'Simple'
    COMPLEJO = 'Complejo'
    
    TIPO = [(SIMPLE, 'Simple'),
                (COMPLEJO, 'Complejo'),]
    tipo_categoria = models.CharField(max_length=20,  choices=TIPO, default= COMPLEJO)
    
    def get_tipo_categoria(self):
        return str(self.tipo_categoria)
    
    def __str__(self):
      return f'{self.tratamiento}'
    
#  return f'{self.categoria_tratamiento} es Tratamiento {self.tipo_categoria}'
    
    # def is_upperclass(self):
    #     return self.tipo_categoria in {self.SIMPLE, self.COMPLEJO}


#TRATAMIENTO ASIGNADO
class TratamientoInsumoAsignado(models.Model):
    id_insumo_asig = models.AutoField(primary_key=True)
    tratamiento = models.ForeignKey(
        Tratamiento, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
    )

    insumo = models.ForeignKey(
        Insumo,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    cantidad = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'TratamientoInsumoAsignado'
        

    def __str__(self):
        return self.id_insumo_asig

    def get_tratamiento(self):
        return self.tratamiento.get_codigo_tratamiento()

    def get_insumo(self):
        return self.insumo.codigo_insumo

