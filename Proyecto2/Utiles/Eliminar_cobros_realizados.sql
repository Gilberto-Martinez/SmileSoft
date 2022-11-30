DO $$
DECLARE var_id_cobro INT = 9;-- Aqui se agrega el id_cobro_contado del registro que se desea eliminar
DECLARE var_id INT ;
	
BEGIN
	SELECT id
	INTO var_id
	FROM public."DetalleCobroContado"
	WHERE cobro_id = var_id_cobro;
	
	raise notice 'Value: %', var_id;
	
	DELETE FROM public."gestion_cobros_detallecobrotratamiento"
	WHERE detalle_cobro_id = var_id;
	
	DELETE FROM public."DetalleCobroContado"
	WHERE id = var_id;
	
	DELETE FROM public."CobroContado"
	WHERE id_cobro_contado = var_id_cobro;
	
END;
$$