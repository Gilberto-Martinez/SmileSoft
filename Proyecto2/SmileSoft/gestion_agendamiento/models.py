from django.db import models
from gestion_administrativo.models import *
from gestion_administrativo.models import Persona
from webapp.models import Usuario
from gestion_tratamiento.models import Tratamiento
from gestion_administrativo.models import Paciente
# from gestion_agendamiento.models import *

# Create your models here.


class Horario (models.Model):
    id_hora = models.AutoField(primary_key=True)
    hora = models.TimeField()
    LUN = 'Lunes'
    MART = 'Martes'
    MIERC = 'Miércoles'
    JUEV = 'Jueves'
    VIER = 'Viernes'

    DIAS = [
        (LUN, 'Lunes'),
        (MART, 'Martes'),
        (MIERC, 'Miércoles'),
        (JUEV, 'Jueves'),
        (VIER, 'Viernes'),
    ]
    dias_atencion = models.CharField(
        max_length=100, choices=DIAS, verbose_name='Días de atención', null=True,)
    # estado = models.BooleanField('Estado', default=True)
#     TM='08:00'
#     TM='09:00'
#     TM='10:00'
#     TM='11:00'
#    hora_atencion=models.CharField(max_length=100,choices=HORAS, verbose_name='Hora de atención',null= True,)

    class Meta(object):
        verbose_name_plural = 'Horario'
    
    
    def __str__(self):
        return str(self.hora)
    
    def get_hora(self):
        return str(self.hora.get_hora())


class Cita(models.Model):
    id_cita=models.AutoField(primary_key=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT)
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
    celular = models.ForeignKey(Persona,null= True, max_length=40, on_delete=models.PROTECT,)
   
    fecha = models.DateField()
   # hora = models.TimeField(null=True)
    
    hora_atencion = models.ForeignKey(Horario, null=True,
                                        on_delete=models.PROTECT,
                                        verbose_name='Hora de atencion')
    
    estado = models.BooleanField('Confirmar cita', default=False)
    
    profesional=models.ForeignKey(EspecialistaSalud, max_length=45,
                                                null=False,
                                                blank= False,
                                                on_delete=models.PROTECT,
                                                verbose_name='Profesional a elegir')
    class Meta(object):
        verbose_name_plural = 'Cita'
        ordering = ['nombre_paciente']
        
        
    # def save(self, *args, **kwargs):
    #     cita_reservada = Cita.objects.filter(hora=self.hora,fecha=self.fecha,estado='True')
    #     if cita_reservada and self.estado == True:
    #         raise Exception('Ya existe una cita reservada a esa hora y en esa fecha')
    #     super(Cita, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.tratamiento_solicitado}  reservada por {self.paciente}| | {self.nombre_paciente}'
    
