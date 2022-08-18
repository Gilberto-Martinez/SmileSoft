UPDATE public."Persona"
	SET es_paciente=True
	WHERE numero_documento IN (SELECT numero_documento
							   FROM public."Persona" as pe
							   JOIN public."Paciente" as pa
							  		ON pe.numero_documento=pa.numero_documento_id);