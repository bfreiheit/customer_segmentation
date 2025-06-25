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

WITH advance_days_per_trip AS (
  SELECT
    s.user_id,
    s.trip_id,
    flights.departure_time::date - CASE WHEN s.trip_id IS NOT NULL THEN s.session_start::date END as date1,
    hotels.check_in_time::date - CASE WHEN s.trip_id IS NOT NULL THEN s.session_start::date END as date2,
    GREATEST(
      flights.departure_time::date - CASE WHEN s.trip_id IS NOT NULL THEN s.session_start::date END,
      hotels.check_in_time::date - CASE WHEN s.trip_id IS NOT NULL THEN s.session_start::date END
    ) AS days_advance_booking
  FROM sessions s
  LEFT JOIN flights USING(trip_id)
  LEFT JOIN hotels USING(trip_id)
)
SELECT
  user_id,
  round(avg(date1)) as date1,
  round(avg(date2)) as date2,
  ROUND(AVG(days_advance_booking)) AS avg_days_advance_booking
FROM advance_days_per_trip
WHERE days_advance_booking IS NOT NULL
GROUP BY user_id
LIMIT 50;

