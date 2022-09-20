-- FUNCTION: public.fn_update_additionals(json, integer, integer)

DROP FUNCTION public.fn_update_additionals(json, integer, integer);

CREATE OR REPLACE FUNCTION public.fn_update_additionals(
	data json,
	hotel integer,
	record_room integer)
    RETURNS table (additionals json)
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
    ROWS 1000
AS $BODY$
DECLARE
	r json ;
	id_add int;
	additional int;
BEGIN 
	FOR r IN  (select * from json_array_elements(data) as d)
	LOOP
		id_add = r->>'id';
		additional = (select id from adicional_adicional where hotel_id =hotel and id=(r->>'adicional')::int);
				
		IF id_add IS NULL THEN 
			IF additional IS NOT NULL THEN 
				INSERT INTO registroadicional_registroadicional(adicional,cantidad,precio_total,tipo_adicional,registro_habitacion_id )    
				values((r->>'adicional')::int,(r->>'cantidad')::int,(r->>'precio_total')::numeric,r->>'tipo_adicional',record_room);
	  		ELSE 
				RAISE EXCEPTION '400,No se encontro adicional %',r->>'adicional';
			END IF;
		ELSE
			UPDATE registroadicional_registroadicional SET cantidad=(r->>'cantidad')::int, precio_total=(r->>'precio_total')::numeric 
			WHERE id=id_add;
		END IF;
    END LOOP;	
	
	RETURN QUERY
	SELECT array_to_json(array_agg(row_to_json(t)))
	FROM (
  			SELECT RA.id,RA.adicional,RA.cantidad,RA.precio_total,RA.tipo_adicional 
			FROM registroadicional_registroadicional RA 
			WHERE RA.registro_habitacion_id = record_room
	) AS t;
	
	
END $BODY$;

ALTER FUNCTION public.fn_update_additionals(json, integer, integer)
    OWNER TO jimmqbyh;