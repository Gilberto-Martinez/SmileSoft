--Ejecutar sobre Database: smilesoft

--Crear funcion 
CREATE OR REPLACE FUNCTION insertar_tabla()
RETURNS TRIGGER AS $$

BEGIN
    IF NEW.es_paciente is true THEN
        INSERT INTO public.Paciente(numero_documento_id)
		VALUES(NEW.numero_documento);
    ELSE
    	IF NEW.es_funcionario is true THEN
        	INSERT INTO public.Funcionario(numero_documento_id)
			VALUES(NEW.numero_documento);
    	ELSE
    		IF NEW.es_personal_salud THEN
        		INSERT INTO public.EspecialistaSalud(numero_documento_id)
				VALUES(NEW.numero_documento);
    		ELSE
    			IF NEW.es_proveedor THEN
        			INSERT INTO public.Proveedor(numero_documento_id)
					VALUES(NEW.numero_documento);
    			END IF;
			END IF;
		END IF;
	END IF;
	RETURN NULL;
END;
$$ LANGUAGE plpgsql;-- Database: smilesoft

--Crear Trigger
CREATE TRIGGER t_insertar_tabla
AFTER INSERT ON Public."Persona" FOR EACH ROW
EXECUTE PROCEDURE insertar_tabla();
