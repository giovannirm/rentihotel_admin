-- FUNCTION: public.fn_reservation_detail_customer(integer)

-- DROP FUNCTION public.fn_reservation_detail_customer(integer);

CREATE OR REPLACE FUNCTION public.fn_reservation_detail_customer(
	id_reservation integer)
    RETURNS TABLE(hotel character varying, direccion character varying, departamento character varying, codigo_reserva character varying, fecha_ingreso date, fecha_salida date, cantidad_nino integer, cantidad_adulto integer, precio_total numeric, nombre character varying, apellido character varying, tipo_documento character varying, numero_documento character varying, correo_electronico character varying, celular character varying, tipo_habitacion character varying, cantidad_habitacion integer) 
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
    ROWS 1000
AS $BODY$	
	BEGIN
		RETURN QUERY
		SELECT 
		H.nombre::CHARACTER VARYING, H.direccion::CHARACTER VARYING,
		DEP.nombre::CHARACTER VARYING,
		RES.codigo_reserva::CHARACTER VARYING, RES.fecha_ingreso::DATE, RES.fecha_salida::DATE , RES.cantidad_nino::INTEGER,  RES.cantidad_adulto::INTEGER, RES.precio_total::NUMERIC,
		C.nombre::CHARACTER VARYING ,C.apellido::CHARACTER VARYING,C.tipo_documento::CHARACTER VARYING,C.numero_documento::CHARACTER VARYING,C.correo_electronico::CHARACTER VARYING,C.celular::CHARACTER VARYING,
		--DET.tipo_habitacion ,
		TH.nombre::CHARACTER VARYING,
		DET.cantidad::INTEGER
		FROM reserva_reserva RES
		INNER JOIN hotel_hotel H ON H.id = RES.hotel_id
		INNER JOIN departamento_departamento Dep ON DEP.id = H.departamento_id
		INNER JOIN registrocliente_registrocliente C ON C.id = RES.registro_cliente_id
		INNER JOIN reservadetalle_reservadetalle DET ON DET.reserva_id = RES.id
		INNER JOIN tipohabitacion_tipohabitacion TH ON TH.hotel_id = H.id and DET.tipo_habitacion = TH.id

		WHERE RES.id = id_reservation;

 	END;
$BODY$;

ALTER FUNCTION public.fn_reservation_detail_customer(integer)
    OWNER TO jimmqbyh;


SELECT * from public.fn_reservation_detail_customer(1)