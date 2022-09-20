-- FUNCTION: public.fn_save_records(json, json, integer, integer, timestamp without time zone)

DROP FUNCTION public.fn_save_records(json, json, integer, integer, timestamp without time zone);

CREATE OR REPLACE FUNCTION public.fn_save_records(
	data_r json,
	data_rh json,
	hotel integer,
	user_id integer,
	now_date timestamp without time zone)
    RETURNS TABLE(additionals json) 
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
    ROWS 1000
AS $BODY$
DECLARE

id_reg int;
f json ;
room int;

BEGIN 
    FOR f IN  (select * from json_array_elements(data_rh) as dh)
	LOOP
		room = (select id from habitacion_habitacion where hotel_id =hotel and id=(f->>'habitacion')::int );
		IF room IS NULL THEN 
			RAISE EXCEPTION '404,No se encontro habitacion %',(f->>'habitacion')::int;
	  	--ELSE
			--RETURN NEXT  r->>'adicional';
		END IF;
    END LOOP;

	INSERT INTO registro_registro(
        hotel_id,
        reserva,
        cliente_id,
        estado_registro,
        tipo_pago,
        adelanto,
        precio_total,
        usuario_registra,
        fecha_registro,
        fecha_actualiza )
	    SELECT 
               hotel,
               (r->>'reserva')::integer,
			   (r->>'cliente')::integer,
			   (r->>'estado_registro')::character varying ,		  
			   (r->>'tipo_pago')::character varying , 
               (r->>'adelanto')::numeric ,
               (r->>'precio_total')::numeric,
               user_id,
			   now_date,
               now_date
        FROM json(data_r) as r  RETURNING id INTO id_reg ;

        
    INSERT INTO registrohabitacion_registrohabitacion(
                registro_id,
	            habitacion,
                estado_habitacion,
                fecha_ingreso,
                fecha_salida,
                codigo, 
                cantidad_adulto, 
                cantidad_nino,               
                precio,
                precio_total,
                tiempo,               
                usuario_registra,
                fecha_registro,
                fecha_actualiza)
	    SELECT 
                id_reg,
                (d->>'habitacion')::integer,
                (d->>'estado_habitacion')::character varying,
                (d->>'fecha_ingreso')::timestamp without time zone,
                (d->>'fecha_salida')::timestamp without time zone,
                (d->>'codigo')::character varying,
                (d->>'cantidad_adulto')::integer,
			    (d->>'cantidad_nino')::integer,
                (d->>'precio')::numeric,  
                (d->>'precio_total')::numeric,          
                (d->>'tiempo')::integer,
                user_id,
			    now_date,
                now_date
    
        FROM json_array_elements(data_rh) as d ;

    RETURN QUERY 
    SELECT row_to_json(t)
        FROM (
                SELECT 
                    R.id,                 		
					R.hotel_id,R.reserva, R.cliente_id, R.estado_registro,
					R.tipo_pago,R.adelanto,R.precio_total,
                    ( 	
                        SELECT array_to_json(array_agg(row_to_json(rs)))
                        FROM (
                                SELECT  RH.id,
										RH.habitacion,RH.estado_habitacion,RH.fecha_ingreso,
										RH.fecha_salida,RH.codigo,RH.tiempo,RH.cantidad_adulto,
										RH.cantidad_nino,RH.precio,RH.precio_total                 
                                FROM registrohabitacion_registrohabitacion RH
                                WHERE RH.registro_id = R.id
                             )
                    AS rs )  AS registros_habitacion            
                FROM registro_registro R 
                WHERE R.id = id_reg
                
            ) AS t;
	
	
END $BODY$;

ALTER FUNCTION public.fn_save_records(json, json, integer, integer, timestamp without time zone)
    OWNER TO jimmqbyh;

