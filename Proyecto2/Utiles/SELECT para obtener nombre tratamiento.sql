SELECT cd.id, cd.tratamiento_id, cd.cobro_contado_id, t.nombre_tratamiento
	FROM public.gestion_cobros_detallecobro cd
	JOIN public."Tratamiento" t
		ON cd.tratamiento_id = t.codigo_tratamiento		
	WHERE cd.cobro_contado_id = '70'
;