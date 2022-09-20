CREATE OR REPLACE FUNCTION public.fn_search_additionals(
	p_hotel integer,
	p_name character varying)
    RETURNS TABLE(id integer, nombre character varying, precio numeric, cantidad integer) 
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
    ROWS 1000
AS $BODY$
	DECLARE
        hotel int;	
	BEGIN
        hotel = (SELECT h.id from hotel_hotel h where h.id = p_hotel);        
        IF hotel IS  NULL THEN 
            RAISE EXCEPTION '404,No se encontro hotel';
        ELSE 
            RETURN QUERY
            SELECT H.id,H.nombre,H.precio,H.cantidad
	        FROM adicional_adicional H
            WHERE H.estado='ACT' AND H.hotel_id =p_hotel  
            AND H.nombre ILIKE p_name||'%' ORDER BY H.nombre LIMIT 10;

        END IF;	
    END;
$BODY$;
