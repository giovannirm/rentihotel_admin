CREATE VIEW reservations AS
SELECT R.id AS reserva, R.fecha_ingreso, R.fecha_salida,count(D.id) AS cant_habitacion ,R.fecha_registro,
R.estado_reserva
FROM reserva_reserva R
INNER JOIN reservadetalle_reservadetalle D ON R.id = D.reserva_id
WHERE NOT R.estado_reserva='PENDIENTE'
GROUP BY R.ID
ORDER BY R.id
