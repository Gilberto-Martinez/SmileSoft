  def detalle_cobro_pdf(request, id_paciente, codigo_tratamiento):
    listado_tratamientos = TratamientoConfirmado.objects.filter(estado='Confirmado')
    paciente = Paciente.objects.get(id_paciente=id_paciente)
    cedula = paciente.numero_documento
    persona = Persona.objects.get(numero_documento=cedula)
    fecha_actual= (datetime.datetime.now().strftime('%d/%m/%Y'))
   
    listado_insumos_asig= TratamientoInsumoAsignado.objects.all()
    
    tratamientos_insumos_asignados = []
    # id_paciente = paciente.id_paciente

    # tratamientos_agendados = []
    insumos = []
    precio_total = 0
    # tratamiento_agendado = {}
    for tratamiento in listado_tratamientos:
        if str(tratamiento.get_paciente()) == str(id_paciente):
            cod_tratamiento = tratamiento.get_tratamiento()
            nuevo_tratamiento = Tratamiento.objects.get(codigo_tratamiento=cod_tratamiento)
            nuevo_insumo= []
            # fecha_actual= datetime.datetime.now().strftime('%d/%m/%Y')
            
            for insumo_asig in listado_insumos_asig:
                if str(insumo_asig.get_tratamiento()) == str(codigo_tratamiento):
                    # id_tratamiento_insumo = tratamiento.id_insumo_asig
                    cod_insumo = insumo_asig.get_insumo()
                    nuevo_insumo = Insumo.objects.get(codigo_insumo=cod_insumo)
                    insumos.append(nuevo_insumo)
            tratamiento_insumo_asig = {
                                        "insumos":insumos,
                                        "tratamiento":nuevo_tratamiento
            }
            tratamientos_insumos_asignados.append(tratamiento_insumo_asig)
        
            precio_total = precio_total + int(nuevo_tratamiento.precio)
            precio_total = '{:,}'.format(precio_total).replace(',','.')
    
    pdf = render_to_pdf("detalle_cobro_pdf.html",{
                                                    'tratamientos_agendados':tratamientos_insumos_asignados,
                                                    'persona':persona,
                                                    'precio_total':precio_total,
                                                    
                                                })
    return HttpResponse(pdf, content_type='application/pdf')
