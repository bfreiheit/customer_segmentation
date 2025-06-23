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
  - `cust_id`
  - `age`
  - `is_married`
  - `has_children`

## Methods
1. **Data cleaning, EDA & Feature Engineering**  
First, several data preparation operations has been done such as missing value treatment, outlier capping, feature reduction and normalization.

   - Umgang mit fehlenden Werten  
   - Normalisierung der numerischen Variablen  
   - Erstellung neuer Features (falls relevant)

2. **Model selection**  
   - Beschreibung der gewählten Clustering-Methode (z. B. `KMeans`)
   - Begründung der gewählten Anzahl Cluster (z. B. Elbow-Methode, Silhouetten-Score)

3. **Evaluation**  
   - Darstellung der gefundenen Clusterzentren
   - Interpretation der Cluster

## Results

| Cluster | Beschreibung                                 | Beispielkunden             |
|---------|---------------------------------------------|----------------------------|
| 0       | Junge Erwachsene, niedrige Ausgaben          | Kunde 101, Kunde 203       |
| 1       | Mittleres Einkommen, hohe Shopping-Frequenz | Kunde 333, Kunde 412       |
| ...     | ...                                         | ...                        |

*Optional*:  
Füge hier auch Plots ein (z. B. Streudiagramm oder Cluster-Visualisierungen) mit einer kurzen Beschreibung.

## Conclusion
- Was lernen wir aus der Segmentierung?
- Wie könnten die Segmente konkret angesprochen werden?
- Weitere Verbesserungsideen (z. B. zusätzliche Features, andere Clustering-Algorithmen)?

---

## References
- [KMeans-Dokumentation (scikit-learn)](https://scikit-learn.org/stable/modules/clustering.html#k-means)
- [Customer Segmentation with Machine Learning: Targeting the Right Audience](https://medium.com/@byanalytixlabs/customer-segmentation-with-machine-learning-targeting-the-right-audience-656f5d2ce8f8)
- [Projekt-Notebook](../notebooks/Segmentation.ipynb)
---

*(updated on: `2025-06-22`)*  
