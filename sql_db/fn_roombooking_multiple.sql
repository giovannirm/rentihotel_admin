----json2----


-- FUNCTION: public.fn_room_booking_multiple_json(integer, date, date, integer[])

DROP FUNCTION public.fn_room_booking_multiple_json(integer, date, date, integer[]);

CREATE OR REPLACE FUNCTION public.fn_room_booking_multiple_json(
	id_hotel integer,
	initial_date date,
	final_date date,
	rooms integer[])
    RETURNS TABLE(additionals json) 
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
    ROWS 1000
AS $BODY$
	DECLARE
	 	sql varchar;
		rooms_h varchar;
		ocupado varchar;
		reservado varchar;		
	BEGIN
	    ocupado = '''OCUPADO''';
		reservado = '''RESERVADO''';
		
		rooms_h = (SELECT array_to_string( rooms , ',')) ;	 	
		sql:= 
	    'SELECT row_to_json(t)
        	FROM (              
                  SELECT RH.habitacion,
				  (SELECT array_to_json(array_agg(row_to_json(rs)))
                   FROM (
                            SELECT RA.registro_id , RA.id AS reg_habitacion_id, RA.habitacion, 
							RA.estado_habitacion, RA.codigo, CAST( RA.fecha_ingreso AS DATE ),
							CAST( RA.fecha_salida AS DATE ) 
							FROM registrohabitacion_registrohabitacion RA
							WHERE RA.habitacion = RH.habitacion'||'
							AND RA.estado_habitacion IN ('||ocupado||','||reservado||')
		    				AND ( CAST( RA.fecha_ingreso AS DATE ) BETWEEN '''||initial_date||''' AND '''||final_date||''' OR 
							CAST( RA.fecha_salida AS DATE ) BETWEEN '''||initial_date||''' AND '''||final_date||''')
						)
                    AS rs) AS registros
				    
					FROM registrohabitacion_registrohabitacion RH
					INNER JOIN registro_registro R ON R.id = RH.registro_id 
					HERE R.hotel_id = '||id_hotel||'AND RA.habitacion IN ('||rooms_h||')'||'
					GROUP BY 1
                
            ) AS t ';

   		RETURN QUERY EXECUTE sql;
   END;
$BODY$;

ALTER FUNCTION public.fn_room_booking_multiple_json(integer, date, date, numeric[])
    OWNER TO jimmqbyh;




	'SELECT array_to_json(array_agg(row_to_json(rs)))
        	FROM (
                SELECT RA.registro_id , RA.id AS reg_habitacion_id, RA.habitacion, 
			    RA.estado_habitacion, RA.codigo, CAST( RA.fecha_ingreso AS DATE ),
				CAST( RA.fecha_salida AS DATE ) 
				FROM registrohabitacion_registrohabitacion RA
				INNER JOIN registro_registro R ON R.id = RA.registro_id 
				WHERE R.hotel_id = '||id_hotel||'AND RA.habitacion IN ('||rooms_h||')'||
		        'AND RA.estado_habitacion IN ('||ocupado||','||reservado||')
		    	AND ( CAST( RA.fecha_ingreso AS DATE ) BETWEEN '''||initial_date||''' AND '''||final_date||''' OR 
				CAST( RA.fecha_salida AS DATE ) BETWEEN '''||initial_date||''' AND '''||final_date||''')   	
				ORDER BY RA.registro_id 
				) AS rs';


































----json1----

-- FUNCTION: public.fn_room_booking_multiple_json(integer, date, date, integer[])

DROP FUNCTION public.fn_room_booking_multiple_json(integer, date, date, integer[]);

CREATE OR REPLACE FUNCTION public.fn_room_booking_multiple_json(
	id_hotel integer,
	initial_date date,
	final_date date,
	rooms integer[])
    RETURNS TABLE(additionals json) 
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
    ROWS 1000
AS $BODY$
	DECLARE
	 	sql varchar;
		rooms_h varchar;
		ocupado varchar;
		reservado varchar;		
	BEGIN
	    ocupado = '''OCUPADO''';
		reservado = '''RESERVADO''';
		
		rooms_h = (SELECT array_to_string( rooms , ',')) ;	 	
		sql:= 
		'SELECT array_to_json(array_agg(row_to_json(rs)))
        	FROM (
                SELECT RA.registro_id , RA.id AS reg_habitacion_id, RA.habitacion, 
			    RA.estado_habitacion, RA.codigo, CAST( RA.fecha_ingreso AS DATE ),
				CAST( RA.fecha_salida AS DATE ) 
				FROM registrohabitacion_registrohabitacion RA
				INNER JOIN registro_registro R ON R.id = RA.registro_id 
				WHERE R.hotel_id = '||id_hotel||'AND RA.habitacion IN ('||rooms_h||')'||
		        'AND RA.estado_habitacion IN ('||ocupado||','||reservado||')
		    	AND ( CAST( RA.fecha_ingreso AS DATE ) BETWEEN '''||initial_date||''' AND '''||final_date||''' OR 
				CAST( RA.fecha_salida AS DATE ) BETWEEN '''||initial_date||''' AND '''||final_date||''')   	
				ORDER BY RA.registro_id 
				) AS rs';

   		RETURN QUERY EXECUTE sql;
   END;
$BODY$;

ALTER FUNCTION public.fn_room_booking_multiple_json(integer, date, date, numeric[])
    OWNER TO jimmqbyh;



SELECT array_to_json(array_agg(row_to_json(rs)))
                   FROM (
                                SELECT  HA.tipo_habitacion_id ,RA.registro_id , RA.id AS reg_habitacion_id, RA.habitacion, 
								 RA.estado_habitacion, RA.codigo, CAST( RA.fecha_ingreso AS DATE ),
								CAST( RA.fecha_salida AS DATE ) 
								FROM registrohabitacion_registrohabitacion RA
								INNER JOIN registro_registro R ON R.id = RA.registro_id 
								INNER JOIN habitacion_habitacion HA ON HA.id = RA.habitacion
								WHERE R.hotel_id=1 and RA.habitacion IN (1,2)
								AND RA.estado_habitacion IN ('OCUPADO','RESERVADO') 
								AND ( CAST( fecha_ingreso AS DATE ) BETWEEN '2020-04-04' AND '2020-05-12' OR CAST( fecha_salida AS DATE ) BETWEEN '2020-04-04' AND '2020-05-12' )
                            	
						)
                    AS 


-----

SELECT row_to_json(t)
        FROM (              
                  SELECT RH.habitacion,
				  (SELECT array_to_json(array_agg(row_to_json(rs)))
                   FROM (
                                SELECT RA.registro_id , RA.id AS reg_habitacion_id, RA.habitacion, 
								 RA.estado_habitacion, RA.codigo, CAST( RA.fecha_ingreso AS DATE ),
								CAST( RA.fecha_salida AS DATE ) 
								FROM registrohabitacion_registrohabitacion RA
								WHERE RA.habitacion = RH.habitacion
								AND RA.estado_habitacion IN ('OCUPADO','RESERVADO') 
								AND ( CAST( fecha_ingreso AS DATE ) BETWEEN '2020-04-04' AND '2020-04-12' OR CAST( fecha_salida AS DATE ) BETWEEN '2020-04-04' AND '2020-05-12' )
                            	
						)
                    AS rs) AS registros
				    
					FROM registrohabitacion_registrohabitacion RH
					INNER JOIN registro_registro R ON R.id = RH.registro_id 
					WHERE R.hotel_id=1 and RH.habitacion IN (1,4) 
					GROUP BY 1
                
            ) AS t ;




--------------------

CREATE OR REPLACE FUNCTION public.fn_room_booking_multiple(
	id_hotel integer,
	id_room integer,
	initial_date date,
	final_date date,
	rooms numeric[])
    RETURNS TABLE(registro_id integer, reg_habitacion_id integer, habitacion integer, estado_habitacion character varying, codigo character varying, fecha_ingreso date,
				  fecha_salida date , tipo_habitacion integer) 
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
    ROWS 1000
AS $BODY$
	DECLARE
	 	sql varchar;
		rooms_h varchar;
		ocupado varchar;
		reservado varchar;
		
	BEGIN
	    ocupado = '''OCUPADO''';
		reservado = '''RESERVADO''';
		
		rooms_h = (SELECT array_to_string( rooms , ',')) ;	 	
		sql:= 'SELECT  RA.registro_id::INTEGER , 
	    		RA.id::INTEGER, 
	   		    RA.habitacion::INTEGER, 
	   		    RA.estado_habitacion::CHARACTER VARYING, 
	   		    RA.codigo::CHARACTER VARYING, 
	   		    CAST( RA.fecha_ingreso AS DATE )::DATE,
	   		    CAST( RA.fecha_salida AS DATE )::DATE ,
				H.tipo_habitacion_id::INTEGER
		FROM registrohabitacion_registrohabitacion RA
		INNER JOIN registro_registro R ON R.id = RA.registro_id 
		INNER JOIN habitacion_habitacion H ON H.id = RA.habitacion
		WHERE R.hotel_id = '||id_hotel||'AND RA.habitacion IN ('||rooms_h||')'||
		'AND RA.estado_habitacion IN ('||ocupado||','||reservado||')
		AND ( CAST( RA.fecha_ingreso AS DATE ) BETWEEN '''||initial_date||''' AND '''||final_date||''' OR 
		CAST( RA.fecha_salida AS DATE ) BETWEEN '''||initial_date||''' AND '''||final_date||''')';
   		RETURN QUERY EXECUTE sql;
   END;
$BODY$;

ALTER FUNCTION public.fn_room_booking_multiple(integer, integer, date, date, numeric[])
    OWNER TO jimmqbyh;










