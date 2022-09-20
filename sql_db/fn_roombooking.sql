-- FUNCTION: public.fn_room_booking(integer, integer, date, date)

-- DROP FUNCTION public.fn_room_booking(integer, integer, date, date);

CREATE OR REPLACE FUNCTION public.fn_room_booking(
	id_hotel integer,
	id_room integer,
	initial_date date,
	final_date date)
    RETURNS TABLE(registro_id integer, reg_habitacion_id integer, habitacion integer, estado_habitacion character varying, codigo character varying, fecha_ingreso date, fecha_salida date) 
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
    ROWS 1000
AS $BODY$
	DECLARE
	 	sql varchar;
	BEGIN
	 	RETURN QUERY
		SELECT  RA.registro_id::INTEGER , 
	    		RA.id::INTEGER, 
	   		    RA.habitacion::INTEGER, 
	   		    RA.estado_habitacion::CHARACTER VARYING, 
	   		    RA.codigo::CHARACTER VARYING, 
	   		    CAST( RA.fecha_ingreso AS DATE )::DATE,
	   		    CAST( RA.fecha_salida AS DATE )::DATE 

		FROM registrohabitacion_registrohabitacion RA
		INNER JOIN registro_registro R ON R.id = RA.registro_id 
		WHERE RA.habitacion=id_room  AND R.hotel_id=id_hotel
		AND RA.estado_habitacion IN ('OCUPADO','RESERVADO')
		AND ( CAST( RA.fecha_ingreso AS DATE ) BETWEEN initial_date AND final_date  OR  CAST( RA.fecha_salida AS DATE ) BETWEEN initial_date AND final_date );
    END;
$BODY$;

ALTER FUNCTION public.fn_room_booking(integer, integer, date, date)
    OWNER TO jimmqbyh;





------------------------

----example consulta

SELECT  RA.registro_id , RA.id AS reg_habitacion_id, RA.habitacion, RA.estado_habitacion, RA.codigo, CAST( RA.fecha_ingreso AS DATE ),CAST( RA.fecha_salida AS DATE ) 
FROM registrohabitacion_registrohabitacion RA
INNER JOIN registro_registro R ON R.id = RA.registro_id 
WHERE RA.habitacion IN (1,4) --AND R.hotel_id=1 
AND RA.estado_habitacion IN ('OCUPADO','RESERVADO') 
AND ( CAST( fecha_ingreso AS DATE ) BETWEEN '2020-04-04' AND '2020-04-12' OR CAST( fecha_salida AS DATE ) BETWEEN '2020-04-04' AND '2020-04-12' )

--order by registro_id

select * from fn_room_booking(1,1,'2020-04-04','2020-04-12')

CREATE OR REPLACE FUNCTION public.fn_room_booking (id_hotel integer,id_room integer,initial_date date, final_date date)
    RETURNS TABLE(
    	registro_id integer,
    	reg_habitacion_id integer, 
    	habitacion integer, 
    	estado_habitacion character varying, 
    	codigo character varying, 
    	fecha_ingreso date, 
    	fecha_salida date) 
    LANGUAGE 'plpgsql'

AS $BODY$
	DECLARE
	 	sql varchar;
	BEGIN
	 	RETURN QUERY
		SELECT  RA.registro_id::INTEGER , 
	    		RA.id::INTEGER, 
	   		    RA.habitacion::INTEGER, 
	   		    RA.estado_habitacion::CHARACTER VARYING, 
	   		    RA.codigo::CHARACTER VARYING, 
	   		    CAST( RA.fecha_ingreso AS DATE )::DATE,
	   		    CAST( RA.fecha_salida AS DATE )::DATE 

		FROM registrohabitacion_registrohabitacion RA
		INNER JOIN registro_registro R ON R.id = RA.registro_id 
		WHERE RA.habitacion=id_room  AND R.hotel_id=id_hotel
		AND RA.estado_habitacion IN ('OCUPADO','RESERVADO')
		AND ( CAST( RA.fecha_ingreso AS DATE ) BETWEEN initial_date AND final_date  OR  CAST( RA.fecha_salida AS DATE ) BETWEEN initial_date AND final_date );
    END;
$BODY$;

















