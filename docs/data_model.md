## Data model for 


**cohort definition**

| criterion | logic | intention |  
| --- | --- | --- |  
| registration time | sign_up_date <= max_session_date - INTERVAL '6 months' | only user with at least 6 months history |  
| activity duration | max_session_date - min_session_date >= 30 | only user with min. one active month |  
| recency | max_session_date - last_trip_date >= 180 | only user without new bookings |  
| time frame restriction | sign_up_date >= max_session_date - INTERVAL '12 months' | only user who registered 12 months ago |


*users with at least one booking:*  
- users are included who registered 6 months ago
- users are excluded who booked within last 6 months 
- users are included who are active for at least 1 month  

*users with no bookings:*
- users are included who have at least ten page clicks  
- users are included who are active for at least 1 month  
- users are included who registered 6 months ago

---
**target groups**

>**1. users are prone to churn -> there last booking is more than six months ago**  

>**2. user who have been active since six months, but did not booked yet**

Further investigation:  

- Check metrics and user ages over time  
- group user by first session month and track activity duration

**revenue-based KPIs**

| metric | description | formula | date type |
| --- | --- | --- |  --- |  
| total_sales | total value of user: distinguish high and low-value user | SUM(hotel + flight cost) | float |  
 

 **travel-based metrics**

 flight_booked and hotel_booked have been transformed to boolean as the count does not align with cnt_trips.


| metric | description | formula | date type | 
| --- | --- | --- |  --- |  
| min_user_date | first session date per user: serves as user cohort | MIN(s.session_start::date) | date |  
| max_user_date | last session date per user | MAX(s.session_start::date) | date |  
| last_trip_date | last booking date per user |  MAX(CASE WHEN s.trip_id IS NOT NULL THEN s.session_start::date END) | date  |  
| last_trip_user_age | days between last session and last booking per user | MAX(s.session_start::date) - last_trip_date | int |   
| days_active_age | how long was the user active | MAX(s.session_start::date) - MIN(s.session_start::date) | int |  