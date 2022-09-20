-- FUNCTION: public.fn_return_value(character varying, integer)

-- DROP FUNCTION public.fn_return_value(character varying, integer);

CREATE OR REPLACE FUNCTION public.fn_return_value(
	n_table character varying,
	p_id integer)
    RETURNS TABLE(nombre character varying) 
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
    ROWS 1000
AS $BODY$
	DECLARE
	 	sql varchar;
	BEGIN
	 	sql := 'SELECT nombre::CHARACTER VARYING FROM '|| n_table ||' WHERE id='||p_id;
	RETURN QUERY EXECUTE sql;
 
   END;
$BODY$;

ALTER FUNCTION public.fn_return_value(character varying, integer)
    OWNER TO jimmqbyh;