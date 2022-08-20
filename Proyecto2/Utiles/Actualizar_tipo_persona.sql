UPDATE public."Persona"
	SET es_paciente=True
	WHERE numero_documento IN (SELECT numero_documento
							   FROM public."Persona" as pe
							   JOIN public."Paciente" as pa
							  		ON pe.numero_documento=pa.numero_documento_id);

UPDATE public."Persona"
	SET es_funcionario=True
	WHERE numero_documento IN (SELECT numero_documento
							   FROM public."Persona" as pe
							   JOIN public."Funcionario" as fu
							  		ON pe.numero_documento=fu.numero_documento_id);

UPDATE public."Persona"
	SET es_especialista_salud=True
	WHERE numero_documento IN (SELECT numero_documento
							   FROM public."Persona" as pe
							   JOIN public."EspecialistaSalud" as es
							  		ON pe.numero_documento=es.numero_documento_id);