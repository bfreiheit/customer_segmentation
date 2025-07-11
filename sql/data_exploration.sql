SELECT 
        trip_id,         
        CASE WHEN check_out_time::date - check_in_time::date <= 0 
        THEN 1 ELSE check_out_time::date - check_in_time::date 
        END as nights, 
        rooms,
        nights,
        hotel_per_room_usd * rooms * nights AS hotel_price       
    FROM hotels  
    WHERE hotel_per_room_usd * rooms * nights < 0;

SELECT 
    trip_id,
    user_id,
    MAX(CASE WHEN cancellation THEN 1 ELSE 0 END) AS is_cancelled,
    MIN(session_start::date) AS trip_date,
    MAX(session_start::date) AS last_trip_date
FROM sessions
WHERE trip_id IS NOT NULL
GROUP BY trip_id, user_id
HAVING MIN(session_start::date) != MAX(session_start::date);

WITH yearmonth AS (
    SELECT 
        TO_CHAR(session_start::date, 'YYYY-MM') AS ym,
        COUNT(DISTINCT user_id) AS cnt_user  
    FROM sessions 
    GROUP BY 1
    ORDER BY 1
)
SELECT 
    ym,
    cnt_user,
    LAG(cnt_user, 12) OVER (ORDER BY ym) AS prev_cnt,
    ROUND(((cnt_user * 1.0 / NULLIF(LAG(cnt_user, 12) OVER (ORDER BY ym), 0)) - 1) * 100, 2) AS perc_change
FROM yearmonth;
