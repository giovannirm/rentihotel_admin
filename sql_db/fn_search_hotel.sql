-- FUNCTION: public.fn_search_hotel(integer, character varying, character varying, integer, character varying, integer)

DROP FUNCTION public.fn_search_hotel_dates(integer, character varying, character varying, integer, character varying, integer);

CREATE OR REPLACE FUNCTION public.fn_search_hotel_dates(
	p_id integer,
	p_fecha_ini date,
	p_fecha_fin date,
	p_huespedes integer,
	p_campo character varying,
	p_departamento integer)
    RETURNS TABLE(id integer, nombre character varying, direccion character varying, image1 character varying, image2 character varying, image3 character varying, clasificacion integer, latitud character varying, longitud character varying, precio numeric) 
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
    ROWS 1000
AS $BODY$
	DECLARE
	 	sql varchar;
		bloqueado varchar;
		ocupado varchar;
		reservado varchar;
		--host varchar;
	
	BEGIN
		bloqueado = '''BLOQUEADO''';
		ocupado = '''OCUPADO''';
		reservado = '''RESERVADO''';

	 	sql := 'SELECT H.id::INTEGER,
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
				 WHERE H.'||p_campo ||'='|| p_id ||' AND  				
				(
				  	SELECT COUNT(HAB.id::INTEGER) FROM habitacion_habitacion HAB
				  	WHERE HAB.hotel_id= H.id      --AND HAB.tipo_habitacion_id = 4
					AND HAB.estado_habitacion !='||bloqueado||'   
					AND HAB.id NOT IN 
						(   
						SELECT  RA.habitacion FROM registrohabitacion_registrohabitacion RA
						INNER JOIN registro_registro R ON R.id = RA.registro_id 
						--INNER JOIN habitacion_habitacion HABI ON HABI.id = RA.habitacion
						--INNER JOIN tipohabitacion_tipohabitacion T ON T.id = HABI.tipo_habitacion_id
						WHERE R.hotel_id= H.id     --AND T.id = 4
						AND RA.estado_habitacion IN ('||ocupado||','||reservado||')
						AND (   CAST( RA.fecha_ingreso AS DATE ) BETWEEN '''|| p_fecha_ini ||''' AND ''' ||p_fecha_fin||'''  OR 
							CAST( RA.fecha_salida AS DATE ) BETWEEN '''||p_fecha_ini||''' AND ''' ||p_fecha_fin||''' )
						)
				) > 0 '	;
		  
	 	IF p_campo = 'id' THEN
			sql := sql ||'OR H.departamento_id ='||p_departamento || 'GROUP BY H.id' ;
		ELSE 
			sql := sql || 'GROUP BY H.id';
   		END IF;			  
		RETURN QUERY EXECUTE sql;
    END;
$BODY$;

ALTER FUNCTION public.fn_search_hotel(integer, character varying, character varying, integer, character varying, integer)
    OWNER TO jimmqbyh;



select * from public.fn_search_hotel_dates(	21,'2020-04-09','2020-04-10',2,	'departamento_id',21)













---------------------  VERSION SIN FECHAS -------------


-- FUNCTION: public.fn_search_hotel(integer, character varying, character varying, integer, character varying, integer)

-- DROP FUNCTION public.fn_search_hotel(integer, character varying, character varying, integer, character varying, integer);

CREATE OR REPLACE FUNCTION public.fn_search_hotel(
	p_id integer,
	p_fecha_ini character varying,
	p_fecha_fin character varying,
	p_huespedes integer,
	p_campo character varying,
	p_departamento integer)
    RETURNS TABLE(id integer, nombre character varying, direccion character varying, image1 character varying, image2 character varying, image3 character varying, clasificacion integer, latitud character varying, longitud character varying, precio numeric) 
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
    ROWS 1000
AS $BODY$
	DECLARE
	 	sql varchar;
		--host varchar;
	
	BEGIN

	 	sql := 'SELECT H.id::INTEGER,
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
				 WHERE H.'||p_campo ||'='|| p_id ;
		  
	 	IF p_campo = 'id' THEN
			sql := sql ||'OR H.departamento_id ='||p_departamento || 'GROUP BY H.id' ;
		ELSE 
			sql := sql || 'GROUP BY H.id';
   		END IF;			  
		RETURN QUERY EXECUTE sql;
    END;
$BODY$;

ALTER FUNCTION public.fn_search_hotel(integer, character varying, character varying, integer, character varying, integer)
    OWNER TO jimmqbyh;