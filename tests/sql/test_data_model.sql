-- test cancellation logic
 with trips as (SELECT     
    user_id,
    s.trip_id,   
    rooms,
    seats,
    cancellation,
    flight_booked,
    hotel_booked  
FROM sessions s
JOIN flights f ON s.trip_id = f.trip_id
JOIN hotels h ON s.trip_id = h.trip_id
WHERE s.trip_id IS NOT NULL
ORDER BY 1
 )
 select user_id,
 trip_id,
 sum(case when flight_booked then 1 else 0 end) flight_booked,
 sum(case when hotel_booked then 1 else 0 end) hotel_booked,
 MAX(CASE WHEN cancellation THEN 1 ELSE 0 END) AS is_cancelled
 from trips
group by 1, 2
order by 1
;
