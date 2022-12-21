SELECT id_factura, sub_nro_factura1, sub_nro_factura2, sub_nro_factura3, nro_factura, razon_social, direccion, fecha, condicion_venta, telefono, total_pagar, iva_5, iva_10, total_iva, estado, numero_documento, cobro_contado_id
	FROM public.gestion_cobros_factura
	ORDER BY 1	
;