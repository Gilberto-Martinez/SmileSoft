DO $$
DECLARE v_cobros CURSOR FOR SELECT dt.detalle_cobro_id, c.id_cobro_contado
							FROM public.gestion_cobros_detallecobrotratamiento dt
							JOIN public."DetalleCobroContado" dc
 								ON dt.detalle_cobro_id = dc.id
							JOIN public."CobroContado" c
									ON dc.cobro_id = c.id_cobro_contado
;

BEGIN
 	FOR cobro IN v_cobros LOOP
 		UPDATE  public.gestion_cobros_detallecobrotratamiento
 		SET cobro_contado_id = cobro.id_cobro_contado
 		WHERE detalle_cobro_id = cobro.detalle_cobro_id;
 	END LOOP;
END;
$$