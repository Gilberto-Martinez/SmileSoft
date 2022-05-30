--Ejecutar sobre Database: smilesoft

--Crear funcion 
CREATE OR REPLACE FUNCTION crear_usuario()
RETURNS TRIGGER AS $$
DECLARE
	v_usuario varchar;
	v_confirmar varchar;
BEGIN
	v_usuario := LOWER(substring(NEW.nombre, 1,1))||LOWER(split_part(NEW.apellido,' ',1));

	IF NEW.es_interno is true OR NEW.es_externo is true THEN
		SELECT 'existe'
		INTO v_confirmar
		FROM webapp_usuario
		WHERE usuario =v_usuario;
		
		IF v_confirmar lIKE 'existe' THEN
			INSERT INTO webapp_usuario(usuario,password ,is_active, is_staff, is_admin, is_superuser, numero_documento_id) --nombre, apellido, direccion, telefono, correo_electronico, 
			VALUES(v_usuario||nextval('sec_digito_usuario'),Sha256('smilesoft') , TRUE, TRUE, FALSE,FALSE ,NEW.numero_documento);
		ELSE 
			INSERT INTO webapp_usuario(usuario,password ,is_active, is_staff, is_admin, is_superuser, numero_documento_id) --nombre, apellido, direccion, telefono, correo_electronico, 
			VALUES(v_usuario,Sha256('smilesoft') , TRUE, TRUE, FALSE,FALSE ,NEW.numero_documento);
		END IF;
	END IF;
	RETURN NULL;
END;
$$ LANGUAGE plpgsql;-- Database: smilesoft

--Crear Trigger
CREATE TRIGGER t_crear_usuario
AFTER INSERT ON Public."Persona" FOR EACH ROW
EXECUTE PROCEDURE crear_usuario();
