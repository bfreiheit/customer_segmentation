CREATE TABLE IF NOT EXISTS customer_features (
    user_id BIGINT PRIMARY KEY,
    -- original features
    age INTEGER NOT NULL,
    has_children BOOLEAN NOT NULL,
    is_married BOOLEAN NOT NULL,
    cnt_trips REAL,
    avg_diff_trip_days REAL,
    days_last_trip INTEGER,
    avg_days_advance_booking REAL,
    avg_travel_days REAL,
    avg_seats REAL,
    avg_checked_bags REAL,
    avg_flight_travel_days REAL,
    avg_distance_km REAL,
    avg_rooms REAL,
    avg_hotel_nights REAL,
    min_signup_date TIMESTAMP,
    avg_session_duration_seconds REAL,
    flight_booked INTEGER,
    hotel_booked INTEGER,
    avg_flight_discount REAL,
    avg_hotel_discount REAL,
    month_active REAL,
    sessions_per_month REAL,
    trips_per_month REAL,
    page_click_per_session REAL,
    trips_per_session REAL,
    avg_booking_value REAL,
    customer_value_per_month REAL,
    flight_booking_value REAL,
    hotel_booking_value REAL,
    cancellation_rate REAL,
    total_discount_rate REAL,
    discount_per_km REAL,
    flight_discount_rate REAL,
    hotel_discount_rate REAL,
    -- transformed metrics
    avg_flight_discount_log REAL,
    flight_discount_rate_log REAL,    
    discount_per_km_log REAL,
    avg_hotel_discount_log REAL,
    hotel_discount_rate_log REAL,
    days_last_trip_log REAL,
    sessions_per_month_log REAL,
    avg_session_duration_seconds_log REAL,
    page_click_per_session_log REAL,
    avg_flight_travel_days_log REAL,
    avg_seats_log REAL,
    avg_checked_bags_log REAL,
    avg_distance_km_log REAL,
    flight_booking_value_log REAL,
    avg_hotel_nights_log REAL,
    hotel_booking_value_log REAL,
    cancellation_rate_log REAL,
    avg_flight_discount_scaled REAL,
    flight_discount_rate_scaled REAL, 
    discount_per_km_scaled REAL,   
    avg_hotel_discount_scaled REAL,
    hotel_discount_rate_scaled REAL,
    age_scaled REAL,
    is_married_scaled REAL,
    has_children_scaled REAL,
    days_last_trip_scaled REAL,
    sessions_per_month_scaled REAL,
    avg_session_duration_seconds_scaled REAL,
    page_click_per_session_scaled REAL,
    avg_flight_travel_days_scaled REAL,
    avg_seats_scaled REAL,
    avg_checked_bags_scaled REAL,
    avg_distance_km_scaled REAL,
    flight_booked_scaled REAL,
    flight_booking_value_scaled REAL,
    avg_rooms_scaled REAL,
    avg_hotel_nights_scaled REAL,
    hotel_booked_scaled REAL,
    hotel_booking_value_scaled REAL,
    cancellation_rate_scaled REAL,
    flight_discount_score REAL,
    hotel_discount_score REAL,
    user_score REAL,
    engagement_score REAL,
    flight_travel_score REAL,
    hotel_travel_score REAL,
    cancellation_score REAL
);
