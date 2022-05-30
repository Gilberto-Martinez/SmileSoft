--------------------- AL INSERTAR -----------------------------
--Ejecutar sobre Database: smilesoft

--Crear funcion 
CREATE OR REPLACE FUNCTION insertar_persona()
RETURNS TRIGGER AS $$

BEGIN
	IF NEW.es_proveedor is true AND NEW.es_personal_salud is true THEN
		RAISE EXCEPTION 'No puede un proveedor ser personal de salud';
	ELSE 
		IF NEW.es_proveedor is true AND NEW.es_funcionario is true THEN
			RAISE EXCEPTION 'No puede un proveedor ser funcionario';
		ELSE
			IF NEW.es_proveedor is true AND NEW.es_paciente is true THEN
				RAISE EXCEPTION 'No puede un proveedor ser paciente';
			ELSE	
				IF NEW.es_paciente is true THEN
        			INSERT INTO public."Paciente"(numero_documento_id)
					VALUES(NEW.numero_documento);
    			END IF;
	
    			IF NEW.es_funcionario is true THEN
        			INSERT INTO public."Funcionario"(numero_documento_id)
					VALUES(NEW.numero_documento);
    			END IF;
	
    			IF NEW.es_personal_salud THEN
    				INSERT INTO public."EspecialistaSalud"(numero_documento_id)
					VALUES(NEW.numero_documento);
    			END IF;
	
    			IF NEW.es_proveedor THEN
    				INSERT INTO public."Proveedor"(numero_documento_id)
					VALUES(NEW.numero_documento);
    			END IF;
			END IF;
		END IF;		
	END IF;
	RETURN NULL;
END;

$$ LANGUAGE plpgsql;-- Database: smilesoft
--Crear Trigger
--SE EJECUTARA CUANDO SE INSERTE UN NUEVO REGISTRO EN LA TABLA PERSONA
CREATE TRIGGER t_insertar_persona
AFTER INSERT ON Public."Persona" FOR EACH ROW
EXECUTE PROCEDURE insertar_persona();

------------------------- AL MODOFICAR ---------------------------------------
--Crear funcion 
--Crear funcion 
CREATE OR REPLACE FUNCTION modificar_persona()
RETURNS TRIGGER AS $$

BEGIN
    IF NEW.es_proveedor is true AND NEW.es_personal_salud is true THEN
		RAISE EXCEPTION 'No puede un proveedor ser personal de salud';
	ELSE 
		IF NEW.es_proveedor is true AND NEW.es_funcionario is true THEN
			RAISE EXCEPTION 'No puede un proveedor ser funcionario';
		ELSE
			IF NEW.es_proveedor is true AND NEW.es_paciente is true THEN
				RAISE EXCEPTION 'No puede un proveedor ser un paciente';
			ELSE	
				IF OLD.es_paciente is false AND NEW.es_paciente is true THEN
       				INSERT INTO public."Paciente"(numero_documento_id)
					VALUES(NEW.numero_documento);
    			END IF;
	
				IF OLD.es_funcionario is false AND NEW.es_funcionario is true THEN
        			INSERT INTO public."Funcionario"(numero_documento_id)
					VALUES(NEW.numero_documento);
    			END IF;
	
    			IF OLD.es_personal_salud is false AND NEW.es_personal_salud is true THEN
    				INSERT INTO public."EspecialistaSalud"(numero_documento_id)
					VALUES(NEW.numero_documento);
    				END IF;
	
    			IF OLD.es_proveedor is false AND NEW.es_proveedor is true THEN
    				INSERT INTO public."Proveedor"(numero_documento_id)
					VALUES(NEW.numero_documento);
    			END IF;
							
				IF OLD.es_paciente is true AND NEW.es_paciente is false THEN
					DELETE FROM public."Paciente"
					WHERE numero_documento_id = NEW.numero_documento;
    			END IF;
	
				IF OLD.es_funcionario is true AND NEW.es_funcionario is false THEN
					DELETE FROM public."Funcionario"
					WHERE numero_documento_id = NEW.numero_documento;
    			END IF;
	
    			IF OLD.es_personal_salud is true AND NEW.es_personal_salud is false THEN
					DELETE FROM public."EspecialistaSalud"
					WHERE numero_documento_id = NEW.numero_documento;
       			END IF;
	
    			IF OLD.es_proveedor is true AND NEW.es_proveedor is false THEN
					DELETE FROM public."Proveedor"
    				WHERE numero_documento_id = NEW.numero_documento;
    			END IF;
			END IF;
		END IF;		
	END IF;
	RETURN NULL;
END;
$$ LANGUAGE plpgsql;-- Database: smilesoft

--Crear Trigger
--SE EJECUTARA CUANDO SE INSERTE UN NUEVO REGISTRO EN LA TABLA PERSONA
CREATE TRIGGER t_modificar_persona
AFTER UPDATE ON Public."Persona" FOR EACH ROW
EXECUTE PROCEDURE modificar_persona();

-------------------------- AL ELIMINAR -------------------------------------
------------- Al eliminiar paciente---------------------------
CREATE OR REPLACE FUNCTION eliminar_persona()
RETURNS TRIGGER AS $$

BEGIN
	UPDATE public."Persona"
	SET es_paciente = false
	WHERE numero_documento = OLD.numero_documento_id;
	
	RETURN NULL;
END;
$$ LANGUAGE plpgsql;-- Database: smilesoft

CREATE TRIGGER t_eliminar_persona
AFTER DELETE ON Public."Paciente" FOR EACH ROW
EXECUTE PROCEDURE eliminar_persona();

---------Al eliminar Funcionario -----------------
CREATE OR REPLACE FUNCTION eliminar_funcionario()
RETURNS TRIGGER AS $$

BEGIN
	UPDATE public."Persona"
	SET es_funcionario = false
	WHERE numero_documento = OLD.numero_documento_id;
	
	RETURN NULL;
END;
$$ LANGUAGE plpgsql;-- Database: smilesoft

CREATE TRIGGER t_eliminar_funcionario
AFTER DELETE ON Public."Funcionario" FOR EACH ROW
EXECUTE PROCEDURE eliminar_funcionario();

------------------ Al eliminar Proveedor -------------------
CREATE OR REPLACE FUNCTION eliminar_proveedor()
RETURNS TRIGGER AS $$

BEGIN
	UPDATE public."Persona"
	SET es_proveedor = false
	WHERE numero_documento = OLD.numero_documento_id;
	
	RETURN NULL;
END;
$$ LANGUAGE plpgsql;-- Database: smilesoft

CREATE TRIGGER t_eliminar_proveedor
AFTER DELETE ON Public."Proveedor" FOR EACH ROW
EXECUTE PROCEDURE eliminar_proveedor();

--------------------- Al eliminar EspecialistaSalud -------------------
CREATE OR REPLACE FUNCTION eliminar_especialistaSalud()
RETURNS TRIGGER AS $$

BEGIN
	UPDATE public."Persona"
	SET es_personal_salud = false
	WHERE numero_documento = OLD.numero_documento_id;
	
	RETURN NULL;
END;
$$ LANGUAGE plpgsql;-- Database: smilesoft

CREATE TRIGGER t_eliminar_especialistaSalud
AFTER DELETE ON Public."EspecialistaSalud" FOR EACH ROW
EXECUTE PROCEDURE eliminar_especialistaSalud();
