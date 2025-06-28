## Data model

**user demographics & status**
| metric | description | formula | data type |
| --- | --- | --- | --- |
| age | Age of the user in years | (md.max_session_date - u.birthdate) / 365 | float |
| has_children | Indicator if the user has children (1 = yes, 0 = no) | CASE WHEN u.has_children THEN 1 ELSE 0 END | int |
| is_married | Indicator if the user is married (1 = yes, 0 = no) | CASE WHEN u.married THEN 1 ELSE 0 END | int |

**loyality**
| metric | description | formula | data type |
| --- | --- | --- | --- |
| min_signup_date | User's earliest signup date | MIN(u.sign_up_date) | date |
| days_active | Active days (from signup to last session) | MAX(s.session_start) - MIN(u.sign_up_date) | int |
| month_active | Active period in months | days_active / 30 | float |

**booking frequency**
| metric | description | formula | data type |
| --- | --- | --- | --- |
| cnt_trips | Total number of trips | SUM(CASE WHEN t.trip_id IS NOT NULL THEN 1 ELSE 0 END) | int |
| trips_per_month | Average number of trips per active month | cnt_trips / month_active | float |
| flight_booked | Counts of flights booked | SUM(CASE WHEN s.flight_booked THEN 1 ELSE 0 END) | int |
| hotel_booked | Counts of hotels booked | SUM(CASE WHEN s.hotel_booked THEN 1 ELSE 0 END) | int |

**engagement**
| metric | description | formula | data type |
| --- | --- | --- | --- |
| days_last_trip | Days since last trip | MAX(s.session_start) - MAX(t.trip_date) | int |
| cnt_sessions | Total number of sessions | COUNT(DISTINCT s.session_id) | int |
| sum_page_clicks | Total number of page clicks | SUM(s.page_clicks) | int |
| sessions_per_month | Average number of sessions per active month | cnt_sessions / month_active | float |
| page_click_per_session | Average page clicks per session | sum_page_clicks / cnt_sessions | float |
| avg_session_duration_seconds | Average session duration in seconds | AVG(d.session_duration_seconds) | float |

**travel characteristics**
| metric | description | formula | data type |
| --- | --- | --- | --- |
| avg_diff_trip_days | Average days between trips | AVG(t.trip_date - t.prev_trip_date) | float |
| avg_days_advance_booking | Average advance booking time in days | AVG(t.trip_start_date - t.trip_date) | float |
| avg_travel_days | Average travel duration in days | AVG(t.travel_days) | float |
| avg_seats | Average number of seats booked | AVG(t.seats) | float |
| avg_checked_bags | Average number of checked bags per trip | AVG(t.checked_bags) | float |
| avg_flight_travel_days | Average number of flight travel days | AVG(t.flight_travel_days) | float |
| avg_distance_km | Average flight distance in km | AVG(6371 * acos(...)) | float |
| sum_distance_km | Total flight distance in km | SUM(6371 * acos(...)) | float |
| avg_rooms | Average number of hotel rooms per trip | AVG(t.rooms) | float |
| avg_hotel_nights | Average number of hotel nights per trip | AVG(t.nights) | float |

**spending & value**
| metric | description | formula | data type |
| --- | --- | --- | --- |
| sum_flight_price | Total flight spending | SUM(t.flight_price) | float |
| sum_hotel_price | Total hotel spending | SUM(t.hotel_price) | float |
| total_booking_value | Total booking value (hotel + flight) | sum_hotel_price + sum_flight_price | float |
| avg_booking_value | Average booking value per trip | total_booking_value / cnt_trips | float |
| customer_value_per_month | Average booking value per active month | total_booking_value / month_active | float |
| flight_booking_value | Average flight booking value | sum_flight_price / total_booking_value |  
| hotel_booking_value | Average hotel booking value | sum_hotel_price / total_booking_value |  

**price sensitivity & discounts**
| metric | description | formula | data type |
| --- | --- | --- | --- |
| sum_flight_discount | Total amount of flight discounts received | SUM(t.flight_price * s.flight_discount_amount) | float |
| sum_hotel_discount | Total amount of hotel discounts received | SUM(t.hotel_price * s.hotel_discount_amount) | float |
| cnt_flight_discount | Count of sessions with flight discount applied | SUM(CASE WHEN s.flight_discount THEN 1 ELSE 0 END) | int |
| cnt_hotel_discount | Count of sessions with hotel discount applied | SUM(CASE WHEN s.hotel_discount THEN 1 ELSE 0 END) | int |
| avg_flight_discount | Average flight discount rate | AVG(s.flight_discount_amount) | float |
| avg_hotel_discount | Average hotel discount rate | AVG(s.hotel_discount_amount) | float |
| total_discount_rate | Total discount rate on all bookings | (sum_flight_discount + sum_hotel_discount) / total_booking_value | float |
| discount_per_km | Flight discount per km traveled | sum_flight_discount / sum_distance_km | float |
| flight_discount_rate | Ratio of discounts per flight bookings | cnt_flight_discount / flight_booked | float |  
| hotel_discount_rate | Ratio of discounts per hotel bookings | cnt_hotel_discount / hotel_booked | float |

**cancellation behaviour**
| metric | description | formula | data type |
| --- | --- | --- | --- |
| cnt_cancellations | Total number of canceled trips | SUM(CASE WHEN t.trip_id IS NOT NULL THEN t.is_cancelled ELSE 0 END) | int |
| cancellation_rate | Share of trips that were cancelled | cnt_cancellations / cnt_trips | float |