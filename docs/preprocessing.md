## Preprocessing steps

return_flight_booked bool -> to calculate costs per user:
case when return_flight_booked then base_fare_usd / seats / 2 
else base_fare_usd / seats end


recency: for business user the last booking can be more recent than family trips
-> criterion: frequency of booking


filter user by session count: >= 5