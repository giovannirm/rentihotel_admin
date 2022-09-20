-- FUNCTION: public.fn_hotels_by_department(integer)

-- DROP FUNCTION public.fn_hotels_by_department(integer);

CREATE OR REPLACE FUNCTION public.fn_hotels_by_department(
	id_departamento integer)
    RETURNS TABLE(id integer, nombre character varying, direccion character varying, image1 character varying, image2 character varying, image3 character varying, clasificacion integer, latitud character varying, longitud character varying, precio numeric) 
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
    ROWS 1000
AS $BODY$	
	BEGIN
		RETURN QUERY
		SELECT H.id::INTEGER,
	   		   H.nombre::CHARACTER VARYING,
			   H.direccion::CHARACTER VARYING,
	   		   H.image1::CHARACTER VARYING,
			   H.image2::CHARACTER VARYING,
	   		   H.image3::CHARACTER VARYING,
	 		   H.clasificacion::INTEGER,
			   H.latitud::CHARACTER VARYING,
			   H.longitud::CHARACTER VARYING,
	 		   MAX(TIEMPO.precio)
	   
	   	FROM hotel_hotel H
	    INNER JOIN tipohabitacion_tipohabitacion TIPO  ON H.id = TIPO.hotel_id
        INNER JOIN tiempo_tiempo TIEMPO ON TIPO.id = TIEMPO.tipo_habitacion_id
	    INNER JOIN departamento_departamento D ON D.id=H.departamento_id 
	    INNER JOIN provincia_provincia P ON P.id=H.provincia_id AND P.departamento_id=H.departamento_id
	    WHERE H.departamento_id = id_departamento
	    GROUP BY H.id;	
 	END;
$BODY$;

ALTER FUNCTION public.fn_hotels_by_department(integer)
    OWNER TO jimmqbyh;
