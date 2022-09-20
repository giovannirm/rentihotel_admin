CREATE FUNCTION public.fn_payment_culqi()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$
	DECLARE 
		BEGIN
            UPDATE reserva_reserva SET estado_reserva = 'RESERVADO' WHERE id = NEW.reserva;
                      
            RETURN NULL;
        END;
$BODY$;

CREATE TRIGGER ins_payment_culqi AFTER INSERT ON pagoculqi_pagoculqi
FOR EACH ROW  EXECUTE PROCEDURE fn_payment_culqi();