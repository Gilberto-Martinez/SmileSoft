from django.db import models
from gestion_administrativo.models import *
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
                                             related_name='tratamiento_set'
                                         )
    # farmacos = []

    
    class Meta:
        verbose_name = ("tratamiento")
        verbose_name_plural = ("tratamientos")
        ordering = ["codigo_tratamiento"]
        db_table = 'Tratamiento'

    def __str__(self):
        return str(self.codigo_tratamiento)

    def get_id(self):
        return str(self.codigo_tratamiento)
        
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

    class Meta:
        db_table = 'TratamientoInsumoAsignado'
        

    # def __str__(self):
    #     return self.id_insumo_asig


# Comentado por el momento a espera de analisis
# class Horario(models.Model):
#     id_horario = models.AutoField(primary_key=True)
#     L = 'Lunes'
#     M = 'Martes'
#     MI = 'Miércoles'
#     J = 'Jueves'
#     V = 'Viernes'
#     S = 'Sábado'
#     DIAS = (
#             (L,'Lunes'),
#             (M, 'Martes'),
#             (MI, 'Miércoles'),
#             (J, 'Jueves'),
#             (V, 'Viernes'),
#             (S, 'Sábado'),
#     )
#     dia = models.CharField(max_length=9, choices=DIAS, null=False, blank=False, verbose_name='Día')
#     hora = models.TimeField(auto_now = False, auto_now_add = False,verbose_name='Hora', null=False, blank=False )

#     class Meta:
#         verbose_name = ("Horario")
#         verbose_name_plural = ("Horarios")
#         db_table = 'Horario'

#INSUMO ASIGNADO
# class TratamientoInsumoAsignado(models.Model):
#     id_insumo_asig = models.AutoField(primary_key=True)
#     tratamiento = models.ForeignKey(
#         Tratamiento, 
#         on_delete=models.CASCADE, 
#         blank=True, 
#         null=True,
#     )

#     insumo = models.ForeignKey(
#         Insumo,
#         on_delete=models.CASCADE,
#         blank=True,
#         null=True,
#         verbose_name='Insumos ConsulDent'
#     )

#     class Meta:
#         db_table = 'TratamientoInsumoAsignado'
#         verbose_name = 'Insumo Asignado al Tratamiento'
#         verbose_name = 'Insumos para el Tratamiento del Paciente'

#     def __str__(self):
#         return self.id_insumo_asig

#     def get_insumo(self):
#         return str(self.insumo.get_codigo_insumo())

#     def get_tratamiento(self):
#         return str(self.tratamiento.codigo_tratamiento)

#     def get_id_insumo(self):
#         return str(self.id_insumo_asig)
