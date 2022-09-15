--Para eliminar un cobro registrado
--En la variable v_id_cobro debe especificarse el id_cobro del cobro que se desea eliminar

DO $$
DECLARE v_id_cobro INT = 62;
BEGIN
	--Elimina el DetalleCobroTratamiento con cid_cobro_contado igual al especificado en la variable v_id_cobro
	DELETE FROM public.gestion_cobros_detallecobrotratamiento
	WHERE id in (SELECT id
				FROM public.gestion_cobros_detallecobrotratamiento
  				WHERE detalle_cobro_id =(SELECT id
										FROM public."DetalleCobroContado"
										WHERE cobro_id= (SELECT id_cobro_contado
														FROM public."CobroContado"
														WHERE id_cobro_contado = v_id_cobro
														)
										)
				) 
;

	--Elimina el Detalle cobro con cobro_id igual al especificado en la variable v_id_cobro
	DELETE FROM public."DetalleCobroContado"
	WHERE cobro_id = v_id_cobro
	;

	--Elimina el CobroContado con id_cobro_contado igual al especificado en la variable v_id_cobro
	DELETE FROM public."CobroContado"
	WHERE id_cobro_contado = v_id_cobro
	;

END;
$$

--Agregar id_cobro_contado a eliminar en el WHERE del Subselect



	
