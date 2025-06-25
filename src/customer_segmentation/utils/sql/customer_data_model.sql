
WITH max_date AS (
    SELECT MAX(session_start::date) AS max_session_date FROM sessions
),
session_duration AS (
        SELECT user_id,      
        session_id,
        EXTRACT(EPOCH FROM (session_end - session_start)) AS session_duration_seconds
        FROM sessions     
),
hotels AS (
    SELECT 
        trip_id,         
        CASE WHEN check_out_time::date - check_in_time::date <= 0 
        THEN 1 ELSE check_out_time::date - check_in_time::date 
        END as nights, 
                
        rooms,      
        hotel_per_room_usd
    FROM hotels            
),

flights AS (
    SELECT 
        trip_id,
        CASE WHEN return_time::date - departure_time::date <= 0 
        THEN 1 
        ELSE return_time::date - departure_time::date 
        END as travel_days,         

        CASE WHEN return_flight_booked 
        THEN ROUND(base_fare_usd / 2, 2)
        ELSE ROUND(base_fare_usd, 2)
        END AS flight_price,
       
        CASE WHEN return_flight_booked 
        THEN ROUND(base_fare_usd / seats / 2, 2) 
        ELSE ROUND(base_fare_usd / seats, 2)
        END AS flight_price_per_person,

        seats,
        base_fare_usd,
        destination_airport_lat,
        destination_airport_lon
    FROM flights        
),
trip_agg AS (
  SELECT 
    trip_id,
    user_id,
    MAX(CASE WHEN cancellation THEN 1 ELSE 0 END) AS is_cancelled,
    MIN(session_start::date) AS trip_date
  FROM sessions
  WHERE trip_id IS NOT NULL
  GROUP BY trip_id, user_id
),
trip_agg_with_lag AS (
  SELECT
    trip_id,
    user_id,
    is_cancelled,
    trip_date,
    LAG(trip_date) OVER (PARTITION BY user_id ORDER BY trip_date) AS prev_trip_date
  FROM trip_agg
),
trip_level AS (
    SELECT t.trip_id,
    t.user_id,
    t.is_cancelled,
    t.trip_date,
    t.prev_trip_date,
    f.seats,
    f.travel_days,
    f.base_fare_usd,
    f.flight_price,
    f.flight_price_per_person,
    f.destination_airport_lat,
    f.destination_airport_lon,
    h.rooms,
    h.nights,
    h.hotel_per_room_usd
    FROM trip_agg_with_lag t
    LEFT JOIN flights f ON t.trip_id = f.trip_id
    LEFT JOIN hotels h ON t.trip_id = h.trip_id
)
SELECT 
    s.user_id,
    -- user info
    (md.max_session_date - u.birthdate::date) / 365 AS age,    
    CASE WHEN u.has_children THEN 1 ELSE 0 END AS has_children,
    -- trip info
    ROUND(COALESCE(SUM(CASE WHEN t.trip_id IS NOT NULL THEN 1 ELSE 0 END), 0)) AS cnt_trips, 
    ROUND(COALESCE(SUM(CASE WHEN t.trip_id IS NOT NULL THEN t.is_cancelled ELSE 0 END), 0)) AS cnt_cancellations,  
    ROUND(COALESCE(AVG(t.trip_date - t.prev_trip_date), 0)) as avg_diff_trip_days,
    COALESCE(MAX(s.session_start::date) - MAX(CASE WHEN t.trip_date IS NOT NULL THEN t.trip_date END), 0) AS last_trip_age,
    MAX(CASE WHEN t.trip_date IS NOT NULL THEN t.trip_date END) AS last_trip_date,
    -- flight info  
    ROUND(COALESCE(SUM(t.seats), 0)) AS sum_seats,
    ROUND(COALESCE(SUM(t.travel_days), 0)) AS sum_travel_days,   
    ROUND(COALESCE(SUM(t.flight_price), 0), 2) AS sum_flight_price, 
    ROUND(COALESCE(AVG(6371 * acos(
        cos(radians(u.home_airport_lat)) * cos(radians(t.destination_airport_lat)) * 
        cos(radians(u.home_airport_lon) - radians(t.destination_airport_lon)) +
        sin(radians(u.home_airport_lat)) * sin(radians(t.destination_airport_lat))
    )), 0)) AS avg_distance_km,
    -- hotel info
    ROUND(COALESCE(SUM(t.rooms), 0)) AS sum_rooms,    
    ROUND(COALESCE(SUM(t.nights), 0)) AS sum_nights,     
    ROUND(COALESCE(SUM(t.hotel_per_room_usd * t.rooms * t.nights), 0), 2) AS sum_hotel_price,    
   -- session info
    COUNT(DISTINCT s.session_id) AS cnt_sessions,
    SUM(s.page_clicks) AS page_clicks,
    MAX(s.session_start::date) AS max_user_date,
    MIN(u.sign_up_date::date) AS min_user_date,   
    MAX(s.session_start::date) - MIN(u.sign_up_date::date) AS days_active_age,  
    ROUND(AVG(d.session_duration_seconds)) AS avg_session_duration_seconds,    
    -- session info for trips
    SUM(CASE WHEN s.flight_booked THEN 1 ELSE 0 END) AS cnt_booked_flights,
    SUM(CASE WHEN s.hotel_booked THEN 1 ELSE 0 END) AS cnt_booked_hotels,    
    SUM(CASE WHEN s.flight_discount THEN 1 ELSE 0 END) AS cnt_flight_discount,
    SUM(CASE WHEN s.hotel_discount THEN 1 ELSE 0 END) AS cnt_hotel_discount,
    ROUND(COALESCE(AVG(s.flight_discount_amount), 0), 2) AS avg_flight_discount,
    ROUND(COALESCE(AVG(s.hotel_discount_amount), 0), 2) AS avg_hotel_discount
FROM sessions s
LEFT JOIN users u ON s.user_id = u.user_id
LEFT JOIN trip_level t on s.trip_id = t.trip_id AND s.user_id = t.user_id
LEFT JOIN session_duration d ON s.session_id = d.session_id AND s.user_id = d.user_id
CROSS JOIN max_date md
WHERE 
    (md.max_session_date - u.birthdate::date) / 365 BETWEEN 18 AND 90
    -- reduce cohort to user who registered within last 1 to 12 months
    AND u.sign_up_date::date >= md.max_session_date - INTERVAL '12 months' 
    AND u.sign_up_date::date <= md.max_session_date - INTERVAL '1 month'   
GROUP BY 
    s.user_id, age, has_children
HAVING
  COUNT(s.session_id) >= 5
  AND (
       -- users with no bookings
       MAX(CASE WHEN t.trip_id IS NOT NULL THEN s.session_start::date END) IS NULL
       -- or users who's last booking was more than 7 days ago
       OR (MAX(s.session_start::date) - MAX(
             CASE WHEN t.trip_id IS NOT NULL THEN s.session_start::date END)) > 7
);
