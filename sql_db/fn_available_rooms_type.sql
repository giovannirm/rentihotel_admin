---

CREATE OR REPLACE FUNCTION public.fn_available_rooms_type (
	hotel  integer,
    type_room integer,
    initial_date date,
	final_date date)

    RETURNS TABLE(
        id integer,
        numero_habitacion  integer,
        numero_piso integer,
        tipo_habitacion integer,
        estado_habitacion character varying) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE 
    ROWS 1000
AS $BODY$
	BEGIN
	 	RETURN QUERY          
            SELECT  
            HAB.id::INTEGER,
            HAB.numero_habitacion::INTEGER,
            HAB.numero_piso::INTEGER,
            HAB.tipo_habitacion_id::INTEGER,
            HAB.estado_habitacion::CHARACTER VARYING          
            FROM habitacion_habitacion HAB
            WHERE HAB.hotel_id= hotel  AND  HAB.tipo_habitacion_id = type_room
            AND HAB.estado_habitacion != 'BLOQUEADO' 
            AND HAB.id NOT IN (   
                SELECT  
                RA.habitacion
                FROM registrohabitacion_registrohabitacion RA
                INNER JOIN registro_registro R ON R.id = RA.registro_id 
                INNER JOIN habitacion_habitacion H ON H.id = RA.habitacion
                INNER JOIN tipohabitacion_tipohabitacion T ON T.id = H.tipo_habitacion_id
                WHERE R.hotel_id= hotel
                AND T.id = type_room
                AND RA.estado_habitacion IN ('OCUPADO','RESERVADO') 
                AND ( CAST( RA.fecha_ingreso AS DATE ) BETWEEN initial_date AND final_date  OR 
                      CAST( RA.fecha_salida AS DATE ) BETWEEN initial_date AND final_date  )
            )
            ORDER BY HAB.ID;
   
    END;
$BODY$;


----------
SELECT  
RA.registro_id ,RA.id AS reg_habitacion_id, 
RA.estado_habitacion AS reg_hab_estado, 
RA.habitacion,
H.numero_habitacion as Numero, T.nombre as Tipo,
H.estado_habitacion AS estado_room,
RA.codigo,CAST( RA.fecha_ingreso AS DATE ),CAST( RA.fecha_salida AS DATE ) 
--RA.fecha_ingreso , RA.fecha_salida 
FROM registrohabitacion_registrohabitacion RA
INNER JOIN registro_registro R ON R.id = RA.registro_id 
INNER JOIN habitacion_habitacion H ON H.id = RA.habitacion
INNER JOIN tipohabitacion_tipohabitacion T ON T.id = H.tipo_habitacion_id
WHERE R.hotel_id=2
AND T.id = 3
AND RA.estado_habitacion IN ('OCUPADO','RESERVADO') 
AND ( CAST( fecha_ingreso AS DATE ) BETWEEN '2020-04-05' AND '2020-04-08' OR CAST( fecha_salida AS DATE ) BETWEEN '2020-04-05' AND '2020-04-08' )


--consultas 

SELECT  
RA.registro_id ,RA.id AS reg_habitacion_id, 
RA.estado_habitacion AS reg_hab_estado, 
RA.habitacion,
H.numero_habitacion as Numero, T.nombre as Tipo,
H.estado_habitacion AS estado_room,
RA.codigo, CAST( RA.fecha_ingreso AS DATE ),CAST( RA.fecha_salida AS DATE ) 
FROM registrohabitacion_registrohabitacion RA
INNER JOIN registro_registro R ON R.id = RA.registro_id 
INNER JOIN habitacion_habitacion H ON H.id = RA.habitacion
INNER JOIN tipohabitacion_tipohabitacion T ON T.id = H.tipo_habitacion_id
WHERE R.hotel_id=1 
AND T.id = 1
AND RA.estado_habitacion IN ('OCUPADO','RESERVADO') 
AND ( CAST( fecha_ingreso AS DATE ) BETWEEN '2020-04-28' AND '2020-04-30' OR CAST( fecha_salida AS DATE ) BETWEEN '2020-04-28' AND '2020-04-30' )

--
SELECT * FROM habitacion_habitacion
WHERE hotel_id=1 and tipo_habitacion_id = 1 and
ID NOT IN (2,6) 

SELECT * FROM public.fn_available_rooms_type(
	1, 
	1, 
	 '2020-04-28', 
	'2020-04-30'
)

--------------
