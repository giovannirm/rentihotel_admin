-- FUNCTION: public.fn_update_recordroom()

-- DROP FUNCTION public.fn_update_recordroom();

CREATE FUNCTION public.fn_record_room()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$
	DECLARE 
		total_amount     numeric; 
		--reservation 	numeric;
	BEGIN
		--reservation = ( SELECT RA.id, R.reserva FROM registrohabitacion_registrohabitacion RA  INNER JOIN registro_registro R ON R.id = RA.registro_id  WHERE RA.id = new.id)

		IF (TG_OP = 'DELETE') THEN 
 			total_amount = (SELECT COALESCE(SUM(precio_total), 0) FROM registrohabitacion_registrohabitacion WHERE registro_id = OLD.registro_id);			
			UPDATE registro_registro SET precio_total = total_amount  WHERE id = OLD.registro_id;

			UPDATE habitacion_habitacion SET estado_habitacion='LIBRE'  WHERE id = OLD.habitacion;

	
 		ELSIF (TG_OP = 'UPDATE') THEN
			IF (OLD.precio_total <> NEW.precio_total) THEN
 				total_amount = (SELECT SUM(precio_total) FROM registrohabitacion_registrohabitacion WHERE registro_id = NEW.registro_id);
				UPDATE registro_registro SET precio_total = total_amount  WHERE id = NEW.registro_id;
			END IF;

			IF ( OLD.estado_habitacion <> NEW.estado_habitacion ) THEN
				IF (NEW.estado_habitacion = 'FINALIZADO') THEN
					UPDATE habitacion_habitacion SET estado_habitacion='LIMPIEZA'  WHERE id = new.habitacion;
				ELSE
					UPDATE habitacion_habitacion SET estado_habitacion=NEW.estado_habitacion  WHERE id = new.habitacion;
				END IF;
			END IF;	

		ELSIF (TG_OP = 'INSERT') THEN  	
			total_amount = (SELECT SUM(precio_total) FROM registrohabitacion_registrohabitacion WHERE registro_id = NEW.registro_id);
			UPDATE registro_registro SET precio_total = total_amount  WHERE id = NEW.registro_id;
			
			IF (NEW.estado_habitacion <> 'RESERVADO') THEN
				UPDATE habitacion_habitacion SET estado_habitacion=NEW.estado_habitacion  WHERE id = new.habitacion;
			END IF;

	 	END IF;
 		 		
	 	RETURN NULL;
	END;
$BODY$;

CREATE TRIGGER ins_upd_del_record_room AFTER INSERT OR UPDATE OR DELETE ON registrohabitacion_registrohabitacion
FOR EACH ROW EXECUTE PROCEDURE fn_record_room();

























-----------------
primera version

CREATE FUNCTION public.fn_update_recordroom()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$
	DECLARE 
		total_amount     numeric; 
 	BEGIN
 		IF (TG_OP = 'DELETE') THEN 
 			total_amount = (SELECT COALESCE(SUM(precio_total), 0) FROM registrohabitacion_registrohabitacion WHERE registro_id = OLD.registro_id);			
			UPDATE registro_registro SET precio_total = total_amount  WHERE id = OLD.registro_id;

			UPDATE habitacion_habitacion SET estado_habitacion='LIBRE'  WHERE id = OLD.habitacion;

	
 		ELSIF (TG_OP = 'UPDATE') THEN  
 			IF  (OLD.estado_habitacion <> NEW.estado_habitacion) THEN
				UPDATE habitacion_habitacion SET estado_habitacion=NEW.estado_habitacion  WHERE id = new.habitacion;
			END IF;

			IF (OLD.precio_total <> NEW.precio_total) THEN
 				total_amount = (SELECT SUM(precio_total) FROM registrohabitacion_registrohabitacion WHERE registro_id = NEW.registro_id);
				UPDATE registro_registro SET precio_total = total_amount  WHERE id = NEW.registro_id;
			END IF;			
					

		ELSIF (TG_OP = 'INSERT') THEN  	
			total_amount = (SELECT SUM(precio_total) FROM registrohabitacion_registrohabitacion WHERE registro_id = NEW.registro_id);
			UPDATE registro_registro SET precio_total = total_amount  WHERE id = NEW.registro_id;
			UPDATE habitacion_habitacion SET estado_habitacion=NEW.estado_habitacion  WHERE id = new.habitacion;

	 	END IF;
 		 		
	 	RETURN NULL;
	END;
$BODY$;
;

CREATE TRIGGER update_recordroom_pricetotal AFTER INSERT OR UPDATE OR DELETE ON registrohabitacion_registrohabitacion
FOR EACH ROW EXECUTE PROCEDURE fn_update_recordroom();
