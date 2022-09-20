-- FUNCTION: public.fn_search_place(character varying)

-- DROP FUNCTION public.fn_search_place(character varying);

CREATE OR REPLACE FUNCTION public.fn_search_place(
	p_word character varying)
    RETURNS TABLE(id integer, p_nombre character varying, p_description character varying, p_campo character varying, p_departamento integer) 
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
    ROWS 1000
AS $BODY$
    BEGIN
		RETURN QUERY		  
          SELECT * FROM ubigeo  --vista
		  WHERE UPPER(nombre) like UPPER(p_word||'%')
		  UNION ALL 
		  SELECT H.id::INTEGER AS pk,H.nombre::CHARACTER VARYING,CONCAT(D.nombre,',',P.nombre,',',Dis.nombre)::CHARACTER VARYING AS Description ,'id'::CHARACTER VARYING AS Campo,h.departamento_id as Departamento
		  FROM hotel_hotel H
          INNER JOIN departamento_departamento D ON D.id=H.departamento_id 
          INNER JOIN provincia_provincia P ON P.id=H.provincia_id AND P.departamento_id=H.departamento_id
          INNER JOIN distrito_distrito Dis ON Dis.id = distrito_id AND Dis.provincia_id=H.provincia_id AND Dis.departamento_id=H.departamento_id
          WHERE UPPER(H.nombre) like UPPER('%'||p_word||'%');     	  		 
    END;
$BODY$;

ALTER FUNCTION public.fn_search_place(character varying)
    OWNER TO jimmqbyh;