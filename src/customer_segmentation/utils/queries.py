

query_user = '''WITH max_date AS (
    SELECT MAX(session_start::date) AS max_session_date FROM sessions
),

hotels AS (
    SELECT 
        trip_id,
        check_out_time::date - check_in_time::date AS nights,
        rooms,         
        hotel_per_room_usd
    FROM hotels
    WHERE 
        check_out_time::date - check_in_time::date BETWEEN 1 AND 30             
),

flights AS (
    SELECT 
        trip_id,
        return_time::date - departure_time::date as travel_days,       
        checked_bags,
        seats,
        base_fare_usd
    FROM flights        
)

SELECT 
    s.user_id,
    (md.max_session_date - u.birthdate::date) / 365 AS age,    
    CASE WHEN u.gender = 'F' THEN 1 ELSE 0 END AS is_female,    
    CASE WHEN u.married THEN 1 ELSE 0 END AS is_married,
    CASE WHEN u.has_children THEN 1 ELSE 0 END AS has_children,

    SUM(CASE WHEN s.trip_id IS NULL THEN 0 ELSE 1 END) AS cnt_trips,
    COUNT(s.session_id) AS cnt_sessions,
    SUM(s.page_clicks) AS page_clicks,

    SUM(CASE WHEN s.cancellation = TRUE THEN 1 ELSE 0 END) AS cnt_cancellations,
    SUM(CASE WHEN s.flight_booked = TRUE THEN 1 ELSE 0 END) AS cnt_booked_flights,
    SUM(CASE WHEN s.hotel_booked = TRUE THEN 1 ELSE 0 END) AS cnt_booked_hotels,
    
    SUM(CASE WHEN s.flight_discount = TRUE THEN 1 ELSE 0 END) AS cnt_flight_discount,
    SUM(CASE WHEN s.hotel_discount = TRUE THEN 1 ELSE 0 END) AS cnt_hotel_discount,
  
    MIN(s.session_start::date) AS min_user_date,
    MAX(s.session_start::date) AS max_user_date,
    MAX(s.session_start::date) - MIN(s.session_start::date) AS days_active_age,
    MAX(CASE WHEN s.trip_id IS NOT NULL THEN s.session_start::date END) AS Last_trip_date,
    MAX(CASE WHEN s.trip_id IS NOT NULL THEN s.session_start::date END) -
    MIN(CASE WHEN s.trip_id IS NOT NULL THEN s.session_start::date END) AS avg_diff_trip_days,

    COALESCE(MAX(s.session_start::date) - 
             MAX(CASE WHEN s.trip_id IS NOT NULL THEN s.session_start::date END), 0) AS last_trip_age,   
    
    COUNT(f.checked_bags) AS cnt_checked_bags,
    ROUND(COALESCE(SUM(f.seats), 0)) AS sum_seats,
    ROUND(COALESCE(SUM(f.travel_days), 0)) AS sum_travel_days,
    ROUND(COALESCE(SUM(f.base_fare_usd * f.seats), 0)) AS sum_base_fare_usd,

    ROUND(COALESCE(SUM(h.nights), 0)) AS sum_nights, 
    COALESCE(SUM(h.hotel_per_room_usd * h.rooms * h.nights), 0) AS sum_hotel_usd    

FROM sessions s
LEFT JOIN users u ON s.user_id = u.user_id
LEFT JOIN flights f ON s.trip_id = f.trip_id
LEFT JOIN hotels h ON s.trip_id = h.trip_id
CROSS JOIN max_date md

WHERE 
    u.sign_up_date::date >= md.max_session_date - INTERVAL '12 months'
    AND CHAR_LENGTH(u.home_airport) = 3
    AND (md.max_session_date - u.birthdate::date) / 365 BETWEEN 18 AND 90

GROUP BY 
    s.user_id, age, is_female, married, has_children

-- exclude new user (< 180 days registered) and user who's trip was within last 6 months
-- and user must be active for at least 30 days 
HAVING
  (
    (MAX(md.max_session_date) - MIN(u.sign_up_date::date)) >= 180
    AND MAX(s.session_start::date) - MIN(s.session_start::date) >= 30
    AND MAX(md.max_session_date) - MAX(
          CASE WHEN s.trip_id IS NOT NULL THEN s.session_start::date END
        ) >= 180
  )
  OR
  (
    COUNT(s.trip_id) = 0
    AND SUM(s.page_clicks) >= 10
    AND MAX(s.session_start::date) - MIN(s.session_start::date) >= 30
    AND (MAX(md.max_session_date) - MIN(u.sign_up_date::date)) >= 180
  );
'''

query_monthly_user = '''
WITH user_month AS (
    SELECT 
        TO_DATE(
        EXTRACT(year FROM session_start)::text || '-' ||
        LPAD(EXTRACT(month FROM session_start)::text, 2, '0') || '-01',
        'YYYY-MM-DD'
        ) AS yearmonth,
        user_id,
        SUM(page_clicks) AS sum_page_clicks,
        COUNT(
            CASE WHEN trip_id IS NOT NULL THEN 1 ELSE 0 END
        )  AS cnt_trips,
        MAX(session_end::date) - MIN(session_start::date) AS days_active
    FROM sessions
    GROUP BY 1, 2
)

SELECT 
    yearmonth,    
    SUM(sum_page_clicks) AS sum_page_clicks,
    SUM(cnt_trips)       AS cnt_trips,
    AVG(days_active)     AS avg_active,
    SUM(days_active)     AS sum_active
FROM user_month
GROUP BY 1;
'''