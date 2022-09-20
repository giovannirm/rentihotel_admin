CREATE FUNCTION public.fn_reservation()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$
	DECLARE 
		room_status          character varying; 
 	BEGIN
		IF (OLD.estado_reserva <> NEW.estado_reserva) THEN			
            UPDATE registro_registro SET estado_registro=NEW.estado_reserva
			WHERE reserva = NEW.id;
		END IF;

		RETURN NULL;
	END;
$BODY$;


CREATE TRIGGER upd_reservation AFTER UPDATE ON reserva_reserva
FOR EACH ROW  EXECUTE PROCEDURE fn_reservation();