-- FUNCTION: public.fn_list_reservations(integer, character varying)

DROP FUNCTION public.fn_list_reservations(integer, character varying);

CREATE OR REPLACE FUNCTION public.fn_list_reservations(
	p_hotel integer,
	p_status character varying)
    RETURNS TABLE(id integer, 
				  codigo_reserva character varying, 
				  fecha_ingreso date, fecha_salida date, 
				  cantidad_habitacion integer, 
				  estado_reserva character varying, 
				  numero_documento character varying) 
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
    ROWS 1000
AS $BODY$
	DECLARE
        pendiente varchar;
	 	sql varchar;
        hotel int;
	
	BEGIN
        hotel = (SELECT h.id from hotel_hotel h where h.id = p_hotel);
        pendiente = '''PENDIENTE''';
        sql := '
                SELECT RES.id::INTEGER, 
				RES.codigo_reserva::CHARACTER VARYING,
                RES.fecha_ingreso::DATE,
                RES.fecha_salida::DATE,                
                SUM(DET.cantidad)::INTEGER,    
				RES.estado_reserva::CHARACTER VARYING,
                (SELECT DISTINCT REG.numero_documento FROM registrocliente_registrocliente REG WHERE REG.id = RES.registro_cliente_id )::CHARACTER VARYING
                FROM public.reserva_reserva RES
                INNER JOIN reservadetalle_reservadetalle DET ON DET.reserva_id = RES.id
                INNER JOIN registrocliente_registrocliente REG ON REG.id = RES.registro_cliente_id
                WHERE UPPER(RES.estado_reserva)!='||pendiente||'  AND RES.hotel_id='||p_hotel ;

        IF hotel IS  NULL THEN 
            RAISE EXCEPTION '404,No se encontro hotel';
        ELSE 
            IF p_status = 'None' THEN
                sql := sql ||' GROUP BY RES.id ORDER BY RES.id DESC' ;
            ELSE 
                sql := sql ||' AND UPPER(RES.estado_reserva) ='''||UPPER(p_status)||''' GROUP BY RES.id ORDER BY RES.id DESC';
            END IF;	
        END IF;
		RETURN QUERY EXECUTE sql;
    END;
$BODY$;

ALTER FUNCTION public.fn_list_reservations(integer, character varying)
    OWNER TO jimmqbyh;

SELECT * from public.fn_list_reservations(2,'RESERVADO')



SELECT RES.id, 
RES.fecha_ingreso,
RES.fecha_salida,
RES.estado_reserva,
SUM(DET.cantidad),
RES.codigo_reserva 
,(SELECT DISTINCT REG.numero_documento FROM registrocliente_registrocliente REG WHERE REG.id = RES.registro_cliente_id )
FROM public.reserva_reserva RES
INNER JOIN reservadetalle_reservadetalle DET ON DET.reserva_id = RES.id
INNER JOIN registrocliente_registrocliente REG ON REG.id = RES.registro_cliente_id
WHERE RES.estado_reserva != 'PENDIENTE' and RES.hotel_id = 2 AND RES.estado_reserva=NULL
GROUP BY RES.id ORDER BY RES.id DESC



--------------


CREATE OR REPLACE FUNCTION public.fn_list_reservations(
	p_hotel integer,
	p_status character varying)
    RETURNS TABLE(id integer, codigo_reserva character varying, fecha_ingreso date, fecha_salida date, cantidad_habitacion integer, estado_reserva character varying, numero_documento character varying) 
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
    ROWS 1000
AS $BODY$
	DECLARE
        pendiente varchar;
	 	sql varchar;
	
	BEGIN
        pendiente = '''PENDIENTE''';
        sql := '
                SELECT RES.id::INTEGER, 
				RES.codigo_reserva::CHARACTER VARYING,
                RES.fecha_ingreso::DATE,
                RES.fecha_salida::DATE,                
                SUM(DET.cantidad)::INTEGER,    
				RES.estado_reserva::CHARACTER VARYING,
                (SELECT DISTINCT REG.numero_documento FROM registrocliente_registrocliente REG WHERE REG.id = RES.registro_cliente_id )::CHARACTER VARYING
                FROM public.reserva_reserva RES
                INNER JOIN reservadetalle_reservadetalle DET ON DET.reserva_id = RES.id
                INNER JOIN registrocliente_registrocliente REG ON REG.id = RES.registro_cliente_id
                WHERE UPPER(RES.estado_reserva)!='||pendiente||'  AND RES.hotel_id='||p_hotel ;
		  
	 	IF p_status = 'None' THEN
			sql := sql ||' GROUP BY RES.id ORDER BY RES.id DESC' ;
		ELSE 
			sql := sql ||' AND UPPER(RES.estado_reserva) ='''||UPPER(p_status)||''' GROUP BY RES.id ORDER BY RES.id DESC';
   		END IF;			  
		RETURN QUERY EXECUTE sql;
    END;
$BODY$;