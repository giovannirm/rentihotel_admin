CREATE OR REPLACE FUNCTION public.fn_save_reservations(
	data_r json,
	data_d json,
	code_r character varying,
	now_date timestamp without time zone)
    RETURNS TABLE(additionals json) 
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
    ROWS 1000
AS $BODY$
DECLARE

id_res int;

BEGIN 
	INSERT INTO reserva_reserva (
        hotel_id, 
	    registro_cliente_id,
        fecha_ingreso,
        fecha_salida,
        hora_llegada,
        estado_reserva, 
        subtotal, 
	    igv,
        precio_total, 
        tipo_pago, 
        adelanto,
        fecha_registro,
        cantidad_adulto,
        cantidad_nino,
		codigo_reserva
        )
        SELECT (r->>'hotel')::integer,
			   (r->>'registro_cliente')::integer,
			   (r->>'fecha_ingreso')::date,
               (r->>'fecha_salida')::date ,
			   (r->>'hora_llegada')::character varying ,
			   (r->>'estado_reserva')::character varying ,
               (r->>'subtotal')::numeric,
               (r->>'igv')::numeric ,
			   (r->>'precio_total')::numeric,
			   (r->>'tipo_pago')::character varying , 
               (r->>'adelanto')::numeric ,
			   now_date,
               (r->>'cantidad_adulto')::integer,
			   (r->>'cantidad_nino')::integer,
			   code_r
        FROM json(data_r) as r  RETURNING id INTO id_res	;

    INSERT INTO reservadetalle_reservadetalle( tipo_habitacion, fecha_registro, reserva_id, tiempo, cantidad, precio_total)
        SELECT 
            (d->>'tipo_habitacion')::integer,
            now_date,
            id_res,
            (d->>'tiempo')::integer,
            (d->>'cantidad')::integer,
    		(d->>'precio_total')::numeric
        FROM json_array_elements(data_d) as d ;

    RETURN QUERY 
    SELECT row_to_json(t)
        FROM (
                SELECT 
                    R.id,
                    R.hotel_id, R.registro_cliente_id,R.fecha_ingreso,R.fecha_salida,
                    R.hora_llegada, R.estado_reserva, R.subtotal, R.igv, R.precio_total, 
                    R.tipo_pago,R.adelanto, R.cantidad_adulto, R.cantidad_nino,
                    ( 	
                        SELECT array_to_json(array_agg(row_to_json(d)))
                        FROM (
                                SELECT D.id, D.tipo_habitacion, D.tiempo, D.cantidad, D.precio_total 
                                FROM reservadetalle_reservadetalle D
                                WHERE D.reserva_id = R.id
                             )
                    AS d )  AS reserva_detalle             
                FROM reserva_reserva R 
                WHERE R.id = id_res
                
            ) AS t ;
	
	
END $BODY$;

ALTER FUNCTION public.fn_update_additionals(json, integer, integer)
    OWNER TO jimmqbyh;










------------------------------
select row_to_json(t)
FROM (
  		SELECT 
		R.ID,
		--R.hotel_id, R.registro_cliente_id,R.fecha_ingreso,R.fecha_salida,
        --R.hora_llegada, R.estado_reserva, R.subtotal, R.igv, R.precio_total, 
        R.tipo_pago,R.adelanto, R.cantidad_adulto, R.cantidad_nino,
		
		(ARRAY_TO_JSON(ARRAY_AGG(ROW_TO_JSON(
			D.*::reservadetalle_reservadetalle
			
		)))) AS reserva_detalle
	
		FROM reserva_reserva R 
		INNER JOIN reservadetalle_reservadetalle D ON D.reserva_id = R.id
		WHERE R.id = 7	
		group by 1
	) AS t

--ARRAY_TO_JSON(ARRAY_AGG(ROW_TO_JSON()))

-----------------
SELECT array_to_json(array_agg(row_to_json(t)))
	FROM (
  			--SELECT D.id, D.tipo_habitacion, D.tiempo, D.cantidad, D.precio_total 
			--FROM reservadetalle_reservadetalle D
			--WHERE D.reserva_id = 7
) AS t;
------------------
select row_to_json(t)
FROM (
  		SELECT 
		--R.hotel_id, R.registro_cliente_id,R.fecha_ingreso,R.fecha_salida,
        --R.hora_llegada, R.estado_reserva, R.subtotal, R.igv, R.precio_total, 
        R.tipo_pago,R.adelanto, R.cantidad_adulto, R.cantidad_nino,
		( 	
			SELECT array_to_json(array_agg(row_to_json(d)))
			FROM (
					  SELECT D.id, D.tipo_habitacion, D.tiempo, D.cantidad, D.precio_total 
					  FROM reservadetalle_reservadetalle D
					  WHERE D.reserva_id = 7
				 )
		AS d ) AS reserva_detalle		
	
		FROM reserva_reserva R 
		--INNER JOIN reservadetalle_reservadetalle D ON D.reserva_id = R.id
		WHERE R.id = 7
		
) AS t

--------------------

