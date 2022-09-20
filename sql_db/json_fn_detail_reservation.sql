CREATE OR REPLACE FUNCTION public.fn_detail_reservation(
	hotel integer,
	reservation integer)
	RETURNS TABLE(additionals json) 
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
    ROWS 1000
AS $BODY$
DECLARE
r  int;

BEGIN 
    r = (SELECT R.id FROM reserva_reserva R where R.hotel_id =hotel AND R.id= reservation AND UPPER(R.estado_reserva)!='PENDIENTE');
	IF r IS NULL THEN 
		RAISE EXCEPTION '404,No se encontro reserva';
	ELSE
		RETURN QUERY
        SELECT row_to_json(t)
        FROM (
                SELECT 
                    R.id,                 		
					R.fecha_ingreso,R.fecha_salida,R.hora_llegada,R.estado_reserva,
					R.codigo_reserva,R.cantidad_adulto,R.cantidad_nino,R.subtotal, 
	    			R.igv,R.precio_total,R.tipo_pago,R.adelanto,
					(
						SELECT row_to_json(C)
						FROM (
							SELECT 
							RC.id,RC.nombre,RC.apellido,RC.tipo_documento,RC.numero_documento,
							RC.genero,RC.edad,RC.celular,RC.correo_electronico
							FROM registrocliente_registrocliente RC
							WHERE id = R.registro_cliente_id
														
						) as C					
					) AS registro_cliente ,
                    ( 	
                        SELECT array_to_json(array_agg(row_to_json(rs)))
                        FROM (
                                SELECT  RD.id, RD.tipo_habitacion,RD.precio_total,
										RD.tiempo,RD.cantidad              
                                FROM reservadetalle_reservadetalle RD
                                WHERE RD.reserva_id = R.id
                             )
                    AS rs )  AS reserva_detalle            
                FROM reserva_reserva R 
                WHERE R.id = reservation
                
            ) AS t;

	END IF;
	
END $BODY$;
