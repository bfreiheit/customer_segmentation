FEATURE_GROUPS = {
    # Flight discounts
    "flight_discount_score": [
        "avg_flight_discount",
        "flight_discount_rate",
        "discount_per_km",
    ],
    # Hotel discounts
    "hotel_discount_score": [
        "avg_hotel_discount",
        "hotel_discount_rate",
    ],
    # User demographics
    "user_score": ["age", "is_married", "has_children"],
    # Engagement
    "engagement_score": [
        "days_last_trip",
        "sessions_per_month",
        "avg_session_duration_seconds",
        "page_click_per_session",
    ],
    # Flight travel features
    "flight_travel_score": [
        "avg_flight_travel_days",
        "avg_seats",
        "avg_checked_bags",
        "avg_distance_km",
        "flight_booked",
        "flight_booking_value",
    ],
    # Hotel travel features
    "hotel_travel_score": [
        "avg_rooms",
        "avg_hotel_nights",
        "hotel_booked",
        "hotel_booking_value",
    ],
    # Cancellations
    "cancellation_score": ["cancellation_rate"],
}
