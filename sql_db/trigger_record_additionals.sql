CREATE FUNCTION public.fn_record_additionals()
	RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$
	DECLARE
        total_amount     numeric; 
 
    BEGIN
		IF (TG_OP = 'DELETE') THEN
		 	UPDATE adicional_adicional SET cantidad = cantidad + OLD.cantidad  WHERE id = OLD.adicional;
		 	
		 	total_amount = (SELECT COALESCE(SUM(precio_total), 0) FROM registroadicional_registroadicional WHERE registro_habitacion_id = OLD.registro_habitacion_id);
		 	
	 		UPDATE registrohabitacion_registrohabitacion SET precio_total = precio + total_amount WHERE id = OLD.registro_habitacion_id;

		ELSIF (TG_OP = 'UPDATE') THEN
		 	UPDATE adicional_adicional SET cantidad = cantidad - (NEW.cantidad - OLD.cantidad) WHERE id = new.adicional;
		 	
		 	total_amount = (SELECT SUM(precio_total) FROM registroadicional_registroadicional WHERE registro_habitacion_id = NEW.registro_habitacion_id);
	 		UPDATE registrohabitacion_registrohabitacion SET precio_total = precio + total_amount  WHERE id = NEW.registro_habitacion_id;
		
		ELSIF (TG_OP = 'INSERT') THEN
			UPDATE adicional_adicional SET cantidad = cantidad - NEW.cantidad  WHERE id = new.adicional;
			
			total_amount = (SELECT COALESCE(SUM(precio_total), 0) FROM registroadicional_registroadicional WHERE registro_habitacion_id = NEW.registro_habitacion_id);
	 		UPDATE registrohabitacion_registrohabitacion SET precio_total = precio + total_amount WHERE id = NEW.registro_habitacion_id;
	
		END IF;
	 
	 	RETURN NULL;
	END;
	$BODY$;
;


CREATE TRIGGER ins_upd_del_record_additionals  AFTER INSERT OR UPDATE OR DELETE ON registroadicional_registroadicional
FOR EACH ROW EXECUTE PROCEDURE fn_record_additionals();
