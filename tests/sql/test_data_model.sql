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