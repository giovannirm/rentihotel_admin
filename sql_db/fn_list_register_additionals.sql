CREATE OR REPLACE FUNCTION fn_list_register_additionals (
	record_room integer)

    RETURNS TABLE(id integer, nombre character varying, cantidad integer, precio_total numeric ,tipo_adicional character varying)  
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
    ROWS 1000
AS $BODY$
    BEGIN
		RETURN QUERY		  
        SELECT RA.id::INTEGER,
               A.nombre::CHARACTER VARYING,
               RA.cantidad::INTEGER,
               RA.precio_total::NUMERIC,
               RA.tipo_adicional::CHARACTER VARYING 
        FROM registroadicional_registroadicional RA 
        INNER JOIN adicional_adicional A ON A.id = RA.adicional
        WHERE RA.registro_habitacion_id = record_room  ORDER BY RA.id;    	  		 
    END;
$BODY$;
