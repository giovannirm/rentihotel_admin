CREATE OR REPLACE FUNCTION public.fn_insert_additionals(
data json,
	hotel integer,
	record_room integer)
    RETURNS table (additionals json)
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
AS $BODY$
DECLARE
	r json ;
	adicional int;
	ad_hotel int;
BEGIN 
	FOR r IN  (select * from json_array_elements(data) as d)
	LOOP
		adicional = r->>'adicional';
		ad_hotel = (select id from adicional_adicional where hotel_id =hotel and id=adicional);
		IF ad_hotel IS NULL THEN 
			RAISE EXCEPTION '400,No se encontro adicional %',adicional;
	  	--ELSE
			--RETURN NEXT  r->>'adicional';
		END IF;
    END LOOP;
	
	INSERT INTO registroadicional_registroadicional(
	adicional,
	cantidad, 
	precio_total,
	tipo_adicional, 
	registro_habitacion_id)    
	SELECT  (data_r->>'adicional')::INTEGER,
			(data_r->>'cantidad')::INTEGER,
			(data_r->>'precio_total')::NUMERIC,
			(data_r->>'tipo_adicional')::CHARACTER VARYING,
			record_room 
	FROM json_array_elements(data) as data_r;
    
	RETURN QUERY
	SELECT array_to_json(array_agg(row_to_json(t)))
	FROM (
  			SELECT RA.id,RA.adicional,RA.cantidad,RA.precio_total,RA.tipo_adicional 
			FROM registroadicional_registroadicional RA 
			WHERE RA.registro_habitacion_id = record_room
	) AS t;
	
	
END $BODY$;
