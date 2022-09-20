-- View: public.ubigeo

-- DROP VIEW public.ubigeo;

CREATE OR REPLACE VIEW public.ubigeo
 AS
 SELECT d.id AS pk,
    d.nombre,
    p.nombre AS description,
    'departamento_id'::character varying AS campo,
    d.id AS departamento
   FROM departamento_departamento d
     JOIN pais_pais p ON p.id = d.pais_id
UNION ALL
 SELECT p.id AS pk,
    p.nombre,
    concat(p.nombre, ',', d.nombre)::character varying AS description,
    'provincia_id'::character varying AS campo,
    p.departamento_id AS departamento
   FROM provincia_provincia p
     JOIN departamento_departamento d ON d.id = p.departamento_id
UNION ALL
 SELECT dis.id AS pk,
    dis.nombre,
    concat(dis.nombre, ',', p.nombre, ',', d.nombre)::character varying AS description,
    'distrito_id'::character varying AS campo,
    dis.departamento_id AS departamento
   FROM distrito_distrito dis
     JOIN provincia_provincia p ON p.id = dis.provincia_id
     JOIN departamento_departamento d ON d.id = dis.departamento_id;

ALTER TABLE public.ubigeo
    OWNER TO jimmqbyh;