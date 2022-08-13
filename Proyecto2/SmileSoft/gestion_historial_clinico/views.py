from gestion_administrativo.models import TratamientoConfirmado
from gestion_historial_clinico.models import *
from gestion_administrativo.models import Paciente


def guardar_historial_clinico(id_tratamiento_conf):
    tratamiento_conf = TratamientoConfirmado.objects.get(id_tratamiento_conf=id_tratamiento_conf)
    paciente_id = tratamiento_conf.get_paciente()
    tratamiento_id = tratamiento_conf.get_tratamiento()
    tratamiento = Tratamiento.objects.get(codigo_tratamiento=tratamiento_id)

    paciente = Paciente.objects.get(id_paciente=paciente_id)

    HistorialClinico.objects.create(tratamiento=tratamiento, paciente=paciente)

