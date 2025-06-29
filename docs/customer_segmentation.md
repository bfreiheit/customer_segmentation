# Customer Segmentation

## Intro
Customer segmentation helps in increasing marketing ROI and response rates. 
Personalized recommendations increase user experience.
Reduce churn by identifying at-risk customers.
It also helps in developing products that fit the customers’ requirements.

There exist two different approaches: 
Manually creating rule-based groups based on basic demographic details like sex, family status, age, or other transaction-related information such as spending or basket size. The benefit of this approach is it is simple to implement and interpretable. The disadvantage is it is static.
ML segmentation requires less manual work as statistical modeling finds complex patterns within the data. This allows for scaling the analysis pipeline and enhance accuracy in results. The downside can be the complexity of the algorithm and interpretability. It is very important to ensure the data are high in quality in order to calculate meaningful cluster.
Both approaches can be combined to enhance interpretability.

## Target audience
The goal is to reach customers in the context of a reward campaign to book a flight, a hotel or both. Hence, the conversation rate and booking rate should be increased. in addition, the churn rate should decrease by targeting user which are at risk to churn.
With different perks, depending on historical user transactions and demographic features, user receive personalized push notifications.

To filter the data based on the potential perks, the user cohort has been determined in the first step using a data modelling process in SQL.


## Data
- **Source**: TravelTide postgres database
- **Variables**: Most important attributes are:

**user demographics & status**
| metric | description | formula | data type |
| --- | --- | --- | --- |
| age | Age of the user in years | (md.max_session_date - u.birthdate) / 365 | float |
| has_children | Indicator if the user has children (1 = yes, 0 = no) | CASE WHEN u.has_children THEN 1 ELSE 0 END | int |
| is_married | Indicator if the user is married (1 = yes, 0 = no) | CASE WHEN u.married THEN 1 ELSE 0 END | int |

**booking frequency**
| metric | description | formula | data type |
| --- | --- | --- | --- |
| flight_booked | Counts of flights booked | SUM(CASE WHEN s.flight_booked THEN 1 ELSE 0 END) | int |
| hotel_booked | Counts of hotels booked | SUM(CASE WHEN s.hotel_booked THEN 1 ELSE 0 END) | int |

**engagement**
| metric | description | formula | data type |
| --- | --- | --- | --- |
| days_last_trip | Days since last trip | MAX(s.session_start) - MAX(t.trip_date) | int |
| sessions_per_month | Average number of sessions per active month | cnt_sessions / month_active | float |
| avg_session_duration_seconds | Average session duration in seconds | AVG(d.session_duration_seconds) | float |
| page_click_per_session | Average page clicks per session | sum_page_clicks / cnt_sessions | float |

**travel characteristics**
| metric | description | formula | data type |
| --- | --- | --- | --- |
| avg_seats | Average number of seats booked | AVG(t.seats) | float |
| avg_checked_bags | Average number of checked bags per trip | AVG(t.checked_bags) | float |
| avg_flight_travel_days | Average number of flight travel days | AVG(t.flight_travel_days) | float |
| avg_distance_km | Average flight distance in km | AVG(6371 * acos(...)) | float |
| avg_rooms | Average number of hotel rooms per trip | AVG(t.rooms) | float |
| avg_hotel_nights | Average number of hotel nights per trip | AVG(t.nights) | float |

**spending & value**
| metric | description | formula | data type |
| --- | --- | --- | --- |
| flight_booking_value | Average flight booking value | sum_flight_price / total_booking_value |  
| hotel_booking_value | Average hotel booking value | sum_hotel_price / total_booking_value |  

**price sensitivity & discounts**
| metric | description | formula | data type |
| --- | --- | --- | --- |
| avg_flight_discount | Average flight discount rate | AVG(s.flight_discount_amount) | float |
| avg_hotel_discount | Average hotel discount rate | AVG(s.hotel_discount_amount) | float |
| discount_per_km | Flight discount per km traveled | sum_flight_discount / sum_distance_km | float |
| flight_discount_rate | Ratio of discounts per flight bookings | cnt_flight_discount / flight_booked | float |  
| hotel_discount_rate | Ratio of discounts per hotel bookings | cnt_hotel_discount / hotel_booked | float |

**cancellation behaviour**
| metric | description | formula | data type |
| --- | --- | --- | --- |
| cancellation_rate | Share of trips that were cancelled | cnt_cancellations / cnt_trips | float |

## Methods
1. **Data cleaning, EDA & Feature Engineering**  
First, several data preparation operations has been done such as missing value treatment, feature reduction and normalization.

   - missing values have been replaced with 0  
   - before normalizing, skewed data have been log transformed (`numpy.log1p`)  
   - for normalizing values the `StandardScaler` from `sklearn` has been applied    
   - after scaling, a dimensionality reduction has been applied using `PCA` (Principal Component Analysis) 

2. **Model selection**  
   - Two different clustering methods have been tested: `KMeans`, `GaussianMixture`
   - The number of cluster has been determined based on the visualization of the Elbow-Method     

3. **Evaluation**  
   - The resulting cluster have been aggregated with mean values of features in order to inspect how well the models have distinguish values between cluster
   Validation scores to compare the quality of cluster models:  
   - The `adjusted_rand_score` (ARI) measures the similarity of cluster assignments
   - The `davies_bouldin_score` "is defined as the average similarity measure of each cluster with its most similar cluster". Lower values indicating better clustering
   - The `calinski_harabasz_score` (Variance Ratio Criterion) "is defined as ratio of the sum of between-cluster dispersion and of within-cluster dispersion.[...] higher Calinski-Harabasz score relates to a model with better defined clusters".  

## Results




## Conclusion
- Was lernen wir aus der Segmentierung?
- Wie könnten die Segmente konkret angesprochen werden?
- Weitere Verbesserungsideen (z. B. zusätzliche Features, andere Clustering-Algorithmen)?

---

## References
- [KMeans-Dokumentation (scikit-learn)](https://scikit-learn.org/stable/modules/clustering.html#k-means)
- [Customer Segmentation with Machine Learning: Targeting the Right Audience](https://medium.com/@byanalytixlabs/customer-segmentation-with-machine-learning-targeting-the-right-audience-656f5d2ce8f8)
- [Project-Notebook](../notebooks/Segmentation.ipynb)
---

*(updated on: `2025-06-22`)*  
