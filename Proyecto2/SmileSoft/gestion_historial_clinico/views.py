from asyncio.windows_events import NULL
from gestion_historial_clinico.models import *
from gestion_administrativo.models import Paciente, PacienteTratamientoAsignado


def guardar_historial_clinico(id_tratamiento_asig):
    tratamiento_asig = PacienteTratamientoAsignado.objects.get(id_tratamiento_asig=id_tratamiento_asig)
    paciente_id = tratamiento_asig.get_paciente()
    tratamiento = tratamiento_asig.get_tratamiento()

    paciente = Paciente.objects.get(id_paciente=paciente_id)

    if paciente.id_historial_clinico is NULL:
        print("El historial es nulo")
        # HistorialClinico.objects.create()
