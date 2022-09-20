CREATE FUNCTION public.fn_record()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$
	DECLARE 
		room_status          character varying; 
 	BEGIN
		IF (TG_OP = 'INSERT') THEN
			IF ( NEW.reserva IS NOT NULL ) THEN
				UPDATE reserva_reserva SET estado_reserva = 'REGISTRADO' WHERE id = NEW.reserva;
			END IF;

		ELSIF (TG_OP = 'UPDATE') THEN
			--IF ( NEW.estado_registro = 'FINALIZADO') THEN
				--room_status = 'FINALIZADO';
			--ELSIF
			IF(NEW.estado_registro = 'REGISTRADO') THEN
				room_status = 'OCUPADO';
			ELSE
				room_status = NEW.estado_registro;
			END IF;

			IF (OLD.estado_registro <> NEW.estado_registro) THEN
				UPDATE registrohabitacion_registrohabitacion SET estado_habitacion=room_status
				WHERE registro_id = NEW.id;
			END IF;

		END IF;
		RETURN NULL;
	END;
$BODY$;

CREATE TRIGGER ins_upd_record AFTER INSERT OR UPDATE ON registro_registro
FOR EACH ROW  EXECUTE PROCEDURE fn_record();