from enum import unique
from django.db import models
from django.db.models.deletion import PROTECT
# from django.contrib.postgres.fields import ArrayField
from django.template.defaultfilters import default
from datetime import date, datetime
import dateutil.relativedelta
from dateutil.relativedelta import relativedelta
from gestion_tratamiento.models import TratamientoInsumoAsignado
from gestion_tratamiento.models import Tratamiento
# from gestion_agendamiento.models import *

# Create your models here.
class Persona(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre (*)')
    apellido = models.CharField(max_length=50,  verbose_name='Apellido (*)')
    numero_documento = models.CharField(primary_key=True, max_length=10, verbose_name='Cedula de identidad')
    direccion = models.CharField(max_length=80,  verbose_name='Dirección')
    telefono = models.CharField(max_length=20,  verbose_name='Telefono')
    correo_electronico = models.EmailField(max_length=35,  verbose_name='Correo electrónico')
    fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento')
    F = 'Femenino'
    M = 'Masculino'
    SEXOS = ((F, 'Femenino'), (M, 'Masculino'))
    sexo = models.CharField(max_length=12, choices=SEXOS, verbose_name='Sexo')
    
    es_funcionario = models.BooleanField(verbose_name='Funcionario', default=False)
    es_especialista_salud = models.BooleanField(verbose_name='Especialista de salud', default=False)
    es_paciente =models.BooleanField(verbose_name='Paciente', default=False)

    class Meta:
        # ordering = ['nombre']
        verbose_name_plural = 'Registro de personas'
        ordering = ["nombre"]
        db_table = 'Persona'

    def __str__(self):
        return self.numero_documento

    def obtener_edad(self):
        fecha_nacimiento = str(self.fecha_nacimiento)
        fecha = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
        edad = relativedelta(datetime.now(), fecha)
        edad = edad.years

        return edad



class Cargo(models.Model):
    nombre = models.CharField(max_length=25, null=False, blank=False, primary_key=True)
    salario = models.BigIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'

    def __str__(self):
        return self.nombre


class Funcionario(models.Model):
    id_funcionario = models.AutoField(primary_key=True)
    numero_documento = models.OneToOneField(
                                                Persona, 
                                                max_length=10, 
                                                null=False, 
                                                blank= False,
                                                on_delete=models.PROTECT,
                                                # verbose_name='Cedula de identidad'
                                            )
    cargos = models.ManyToManyField(Cargo, 
                                    through='FuncionarioCargo',
                                    related_name='funcionario_set',
                                    blank=True)


    class Meta:
        # ordering = ['nombre']
        verbose_name_plural = 'Funcionarios'
        db_table = 'Funcionario'

    def __str__(self):
        return str(self.numero_documento)

class FuncionarioCargo(models.Model):
    funcionario = models.ForeignKey(
        Funcionario, 
        on_delete=models.CASCADE, 
        blank=True, null=True
    )

    cargo= models.ForeignKey(
        Cargo,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'FuncionarioCargo'
        verbose_name = 'Cargo de empleado'
        verbose_name = 'Cargos de empleado'


class Especialidad(models.Model):
    id_especialidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=25, null=False, blank=False)

    class Meta:
        verbose_name = ("Especialidad")
        verbose_name_plural = ("Especialidades")
        db_table = 'Especialidad'

    def __str__(self):
        return self.nombre

class EspecialistaSalud(models.Model):
    id_especialista_salud = models.AutoField(primary_key=True)
    numero_documento = models.OneToOneField(
                                                Persona, 
                                                max_length=10, 
                                                null=False, 
                                                blank= False,
                                                on_delete=models.PROTECT,
                                            )
    especialidades = models.ManyToManyField(Especialidad, 
                                    through='EspecialistaEspecialidades',
                                    related_name='especialista_set',
                                    blank=True
                                    )

    class Meta:
        verbose_name = 'Especialista de salud'
        verbose_name_plural = 'Especialistas de salud'
        db_table = 'EspecialistaSalud'

    def __str__(self):
        return str(self.numero_documento.nombre+ ' '+self.numero_documento.apellido)
   

class EspecialistaEspecialidades(models.Model):
    especialista_salud = models.ForeignKey(
        EspecialistaSalud,
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    especialidad = models.ForeignKey(
        Especialidad,
        on_delete=models.CASCADE,
        blank=True, null=True
    )

    class Meta:
        verbose_name = ("Especialdad de especialista")
        verbose_name_plural = ("Especialidades de especialistas")
        db_table = 'EspecialistaEspecialidades'


class Paciente(models.Model):
    id_paciente = models.AutoField(primary_key=True)
    numero_documento = models.OneToOneField(
                                            Persona, max_length=10, 
                                            null=False, 
                                            blank= False,  
                                            on_delete=models.PROTECT,
                                        )
    enfermedad_base = models.TextField(max_length=500, verbose_name='Enfermedad de base (*)',null= True,blank=True)
    alergia = models.TextField(max_length=500,  verbose_name='Alergia (*)',null= True, blank=True)
    tolerancia_anestecia = models.BooleanField(verbose_name='¿Es tolerante al uso de Anestecia?', null= True, blank=True)
    frecuencia_higiene_bucal = models.PositiveIntegerField(null= True, blank=True)
    medicamento = models.CharField(max_length=60,  verbose_name='Medicamento/s (*)',null= True,blank=True)
    cirugias = models.BooleanField(default=False, verbose_name='Cirugías',null= True, blank=True)
    caries = models.BooleanField(default=False, verbose_name='Caries',null= True, blank=True)
    afeccion_cronica_familiar = models.TextField(max_length=500,  verbose_name='Afección crónica familiar',null= True, blank=True)
    NN = 'No especificado'
    AP = 'A RH+'
    AN = 'A Rh-'
    BP = 'B RH+'
    BN = 'B RH-'
    OP = '0 RH+'
    ON = '0 RH-'
    ABP = 'AB RH+'
    ABN = 'AB RH-'
    GRUPOS = [
            (NN, 'No especificado'),
            (AP, 'A RH+'),
            (AN, 'A Rh-'),
            (BP, 'B RH+'),
            (BN, 'B RH-'),
            (OP, '0 RH+'),
            (ON, '0 RH-'),
            (ABP, 'AB RH+'),
            (ABN, 'AB RH-'),
    ]
    grupo_sanguineo = models.CharField(max_length=100,choices=GRUPOS , verbose_name='Grupo sanguíneo',null= True,)
    tratamientos = models.ManyToManyField(
                                            Tratamiento, 
                                             through='PacienteTratamientoAsignado',
                                             related_name='paciente_set'
                                         )

    class Meta:
        verbose_name = ("paciente")
        verbose_name_plural = ("pacientes")
        ordering = ["numero_documento"]
        db_table = 'Paciente'

    def __str__(self):
        return str(self.numero_documento)

    def get_id(self):
        return str(self.id_paciente)

#TRATAMIENTO ASIGNADO
class PacienteTratamientoAsignado(models.Model):
    """"
    Clase que contiene los tratamientos que son asignados al paciente de parte del Odontologo
    de manera pueda agendarse citas para estos tratamientos. Esta clase contendrá registros temporales,
    una vez agendada la cita para el tratamiento en cuestión el registro del mismo es eliminado automaticamente
    """
    id_tratamiento_asig = models.AutoField(primary_key=True)
    paciente = models.ForeignKey(
        Paciente, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
    )

    tratamiento = models.ForeignKey(
        Tratamiento,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Tratamientos ConsulDent'
    )

    class Meta:
        db_table = 'PacienteTratamientoAsignado'
        verbose_name = 'Tratamieto Asignado al Paciente'
        verbose_name = 'Tratamietos del Paciente'

    def __str__(self):
        return self.id_tratamiento_asig

    def get_tratamiento(self):
        return str(self.tratamiento.get_codigo_tratamiento())

    def get_paciente(self):
        return str(self.paciente.id_paciente)

    def get_id_tratamiento(self):
        return str(self.id_tratamiento_asig)


class TratamientoConfirmado(models.Model):
    id_tratamiento_conf = models.AutoField(primary_key=True)
    paciente = models.ForeignKey(
        Paciente, 
        on_delete=models.PROTECT, 
        blank=False, 
        null=False,
    )

    tratamiento = models.ForeignKey(
        Tratamiento,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
    )

    especialista = models.ForeignKey(
        EspecialistaSalud,
        on_delete=models.PROTECT,
        blank=False,
        null=True,
    )
    A = 'Agendado' # Cuando el paciente pide una cita para el tratamiento en cuestión 
    C = 'Confirmado' # Cuando el paciente confirma la cita para el tratamiento en cuestión
    P = 'Pagado'# Una vez que el paciente paga por su tratamiento
    R = 'Realizado'# Al haberle realizado el tratamiento al paciente
    ESTADOS = ((A, 'Agendado'), (C, 'Confirmado'), (P, 'Pagado'), (R, 'Realizado'), )
    estado = models.CharField(max_length=12, choices=ESTADOS, default='Agendado')
    id_cita = models.IntegerField(null=True, unique=True)
    
  

    class Meta:
        db_table = 'TratamientoConfirmado'

    def __str__(self):
        return self.id_tratamiento_conf

    def get_tratamiento(self):
        return str(self.tratamiento.get_codigo_tratamiento())
    
    def get_paciente(self):
        return str(self.paciente.id_paciente)

    def get_estado(self):
        return str(self.estado)

    def get_id_tratamiento(self):
        return str(self.id_tratamiento_conf)
    
    # def get_insumo_asig(self):
    #     return str(self.tratamiento.get_insumo_asig)




#####################################################################

class Proveedor(models.Model):
    ruc = models.CharField(max_length=12, null=False, blank= False, primary_key=True,)
    nombre = models.CharField(max_length=40, null=False, blank= False)
    direccion = models.CharField(max_length=50, null=False, blank= False, verbose_name='Dirección')
    telefono = models.CharField(max_length=20, null=False, blank= False, verbose_name='Teléfono')
    correo_electronico = models.EmailField(max_length=35,  verbose_name='Correo electrónico')
    digito_verificador = models.PositiveIntegerField(verbose_name="Digito verificador", null=True)
    # producto = models.ManyToManyField(Insumo, through='InsumosProveidos')

    class Meta:
        # ordering = ['nombre']
        verbose_name_plural = 'Proveedores'
        db_table = 'Proveedor'

    def __str__(self):
        return str(self.ruc)

# class InsumosProveidos(models.Model):
#     ruc = models.ForeignKey(
#                             Proveedor, 
#                             on_delete=models.PROTECT, 
#                             blank=True, null=True
#     )

#     codigo= models.ForeignKey(
#                                 Insumo,
#                                 on_delete=models.PROTECT,
#                                 blank=True,
#                                 null=True
#     )

#     class Meta:
#         verbose_name_plural = 'Insumos proveidos'
#         db_table = 'InsumoProveido'
 