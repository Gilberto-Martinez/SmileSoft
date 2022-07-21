from django.db import models
from gestion_administrativo.models import *
from gestion_administrativo.models import Persona
from webapp.models import Usuario
from gestion_tratamiento.models import Tratamiento
from gestion_administrativo.models import Paciente
# Create your models here.

class Cita(models.Model):
    id_cita=models.AutoField(primary_key=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    nombre_paciente = models.CharField(max_length=40,
                                      verbose_name='Nombre del Paciente',null=True)
    apellido_paciente = models.CharField(max_length=40,
                                      verbose_name='Apellido del Paciente',null=True)
    tratamiento_solicitado=models.ForeignKey(
                                                Tratamiento,
                                                max_length=45,
                                                null=False,
                                                blank= False,
                                                on_delete=models.PROTECT,
                                                verbose_name='Motivo de consulta'
    )
   
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.BooleanField('Estado', default=True)
    
    profesional=models.ForeignKey(Especialidad, max_length=45,
                                                null=False,
                                                blank= False,
                                                on_delete=models.PROTECT,
                                                verbose_name='Profesional a elegir')
    class Meta(object):
        verbose_name_plural = 'Cita'
        
     

    def __str__(self):
        return f'{self.tratamiento_solicitado}  reservada por {self.paciente}| | {self.nombre_paciente}'
    
