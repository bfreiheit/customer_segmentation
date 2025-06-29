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
- **Features**:  

| Feature Group            | Features                                                                 |
|--------------------------|---------------------------------------------------------------------------|
| flight_discount_score    | - avg_flight_discount<br>- flight_discount_rate<br>- discount_per_km     |
| hotel_discount_score     | - avg_hotel_discount<br>- hotel_discount_rate                            |
| user_score               | - age<br>- is_married<br>- has_children                                   |
| engagement_score         | - days_last_trip<br>- sessions_per_month<br>- avg_session_duration_seconds<br>- page_click_per_session |
| flight_travel_score      | - avg_flight_travel_days<br>- avg_seats<br>- avg_checked_bags<br>- avg_distance_km<br>- flight_booked<br>- flight_booking_value |
| hotel_travel_score       | - avg_rooms<br>- avg_hotel_nights<br>- hotel_booked<br>- hotel_booking_value |
| cancellation_score       | - cancellation_rate                                                      |


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

![Segmentation-Table](../data/segmentation_table.png)


## Conclusion
- Both clustering models performed well on the scaled feature groups. Redundant and high correlated features must be excluded. This process is iterative and with each new feature group the models needs to be inspected. In order to find the targeted segments, the models performed best when features have been separated by flight and hotel user. Overall travel features have been therefore excluded.
- Based on the resulting segments, the different perks of the reward program can be applied to the targeted user groups:
1. free hotel meal -> frequent hotel traveller  
2. free checked bags -> frequent flight traveller  
3. no cancellation fees -> frequent traveller with cancellations  
4. exclusive flight discounts -> flight discount hunter  
5. exclusive hotel discounts -> hotel discount hunter  
6. 1 night free hotel with flight -> churn-risk users  

- other cluster models like DBSCAN or `AgglomerativeClustering` could not be tested due to performance issues (these algorithms need high RAM power). The same is true for the `silhouette_score`.

---

## References
- [KMeans-Dokumentation (scikit-learn)](https://scikit-learn.org/stable/modules/clustering.html#k-means)
- [Customer Segmentation with Machine Learning: Targeting the Right Audience](https://medium.com/@byanalytixlabs/customer-segmentation-with-machine-learning-targeting-the-right-audience-656f5d2ce8f8)
- [Segmentation-Notebook](../notebooks/Segmentation.ipynb)  
- [EDA-Notebook](../notebooks/EDA.ipynb)
---

*(updated on: `2025-06-29`)*  
