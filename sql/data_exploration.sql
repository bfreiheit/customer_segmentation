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

select to_char(session_start::date, 'YYYY-MM'),
count(distinct user_id) as cnt_user  
from sessions 
group by 1
order by 1;