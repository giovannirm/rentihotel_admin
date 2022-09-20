CREATE OR REPLACE FUNCTION fn_register_rclient(
	hotel integer,
	rc_id integer,
	rc_num_doc character varying,
	user_id integer,
	now_date timestamp without time zone,
	OUT id_c integer)
    RETURNS integer
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
AS $BODY$
	DECLARE
        client          integer; 
	BEGIN
    	client = ( SELECT DISTINCT C.id FROM cliente_cliente C INNER JOIN registro_registro R ON R.cliente_id = C.id
				   WHERE R.hotel_id = hotel   and C.numero_documento= rc_num_doc );

    	IF (client IS NULL) THEN
			INSERT INTO cliente_cliente(nombre, apellido, tipo_documento,numero_documento, genero, edad, celular,correo_electronico ,usuario_registra,fecha_registro,fecha_actualiza) 
    		SELECT  RC.nombre, RC.apellido, RC.tipo_documento, RC.numero_documento, RC.genero, RC.edad, RC.celular, RC.correo_electronico , user_id, now_date ,now_date
			FROM registrocliente_registrocliente RC WHERE RC.id = rc_id RETURNING ID into id_c;			
    		 
    	ELSE
			UPDATE cliente_cliente SET 
			nombre = RC.nombre,
			apellido = RC.apellido,
			tipo_documento = RC.tipo_documento,
			numero_documento = RC.numero_documento,
			genero = RC.genero,
			edad = RC.edad,
			celular = RC.celular,
			correo_electronico = RC.correo_electronico,
			usuario_actualiza = user_id,
			fecha_actualiza = now_date
			FROM  registrocliente_registrocliente RC
			where cliente_cliente.id = client  and RC.id=rc_id RETURNING cliente_cliente.id into id_c;
	END IF;
	END;
	$BODY$;

SELECT public.fn_register_rclient(1,5,'70230000',1,'2020-04-01 11:13:50')	
--select * from fn_register_rcliente(2,5,'70230000',1,'2020-04-01 11:13:50')