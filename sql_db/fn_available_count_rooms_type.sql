CREATE OR REPLACE FUNCTION public.fn_available_count_rooms_type(
	hotel  integer,
    initial_date date,
	final_date date)

    RETURNS TABLE(
        tipo_habitacion integer,
        cantidad_habitacion  integer) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE 
    ROWS 1000
AS $BODY$
	BEGIN
	 	RETURN QUERY          
            SELECT  	
            HAB.tipo_habitacion_id::INTEGER,
			COUNT(HAB.id)::INTEGER                       
            FROM habitacion_habitacion HAB
            WHERE HAB.hotel_id= hotel 
            AND HAB.estado_habitacion != 'BLOQUEADO' 
            AND HAB.id NOT IN (   
                SELECT  
                RA.habitacion
                FROM registrohabitacion_registrohabitacion RA
                INNER JOIN registro_registro R ON R.id = RA.registro_id 
                INNER JOIN habitacion_habitacion H ON H.id = RA.habitacion
                INNER JOIN tipohabitacion_tipohabitacion T ON T.id = H.tipo_habitacion_id
                WHERE R.hotel_id= hotel
                AND RA.estado_habitacion IN ('OCUPADO','RESERVADO') 
                AND ( CAST( RA.fecha_ingreso AS DATE ) BETWEEN initial_date AND final_date  OR 
                      CAST( RA.fecha_salida AS DATE ) BETWEEN initial_date AND final_date  )
            )
            GROUP BY HAB.tipo_habitacion_id;
    END;
$BODY$;


SELECT * FROM public.fn_available_count_rooms_type(1, '2020-04-06', '2020-04-30')

