UPDATE public."Insumo"
	SET unidad='Paquete/s'
	WHERE unidad Like 'Paquete' or unidad like 'Paquetes';
	
UPDATE public."Insumo"
	SET unidad='Caja/s'
	WHERE unidad like 'Caja' or unidad like 'Cajas';
	
UPDATE public."Insumo"
	SET unidad='Litro/s'
	WHERE unidad like 'Litro' or unidad like 'Litros';