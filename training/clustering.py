import numpy as np
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler

from typing import Tuple

class Clustering:
    """
    A class to perform KMeans clustering on a dataset with data preprocessing steps
    like scaling and handling missing values.
    
    Attributes:
    data : pd.DataFrame
        The dataset containing features to be clustered.
    selected_features : list
        A list of selected feature names to be used for clustering.
    number_of_clusters : int
        The number of clusters for KMeans clustering.
    random_state : int
        A seed for reproducibility of the KMeans clustering algorithm.
    
    Methods:
    filter_out_dataframe():
        Preprocesses the data by scaling, handling missing values, and returning the final processed data.
    fit() -> Tuple[KMeans, np.ndarray, np.ndarray]:
        Fits the KMeans model on the preprocessed data and returns the trained model, labels, and centroids.
    """
    
    def __init__(self,
                 data: pd.DataFrame,
                 selected_features: list,
                 number_of_clusters: int,
                 random_state: int):
        """
        Initializes the Clustering class with the given dataset, selected features, 
        number of clusters, and random state for reproducibility.
        
        Parameters:
        data (pd.DataFrame): The dataset containing the features to cluster.
        selected_features (list): List of feature names to include in the clustering.
        number_of_clusters (int): The number of clusters for the KMeans algorithm.
        random_state (int): Random seed for reproducibility of clustering results.
        """
        self.data = data
        self.selected_features = selected_features
        self.number_of_clusters = number_of_clusters
        self.random_state = random_state

    def filter_out_dataframe(self):
        """
        Preprocesses the data by handling missing values and scaling the features.
        
        - Extracts the selected features from the original dataframe.
        - Replaces infinite values with NaN.
        - Scales the features to a specified range of 1 to 10.
        - Imputes missing values using the median value of each column.
        
        Returns:
        X_final (np.ndarray): The processed and scaled data with missing values imputed.
        """
        # Extract useful info only
        X = self.data[self.selected_features]
        X.replace([np.inf, -np.inf], np.nan, inplace=True)

        # Scaling 
        scale = MinMaxScaler(feature_range=(1, 10))
        X_scaled = scale.fit_transform(X.values)

        # Replacing NaN with median
        imputer = SimpleImputer(strategy='median')
        X_final = imputer.fit_transform(X=X_scaled)

        return X_final
    
    def fit(self) -> Tuple[KMeans, np.ndarray, np.ndarray]:
        """
        Fits a KMeans clustering model on the preprocessed data and returns the results.
        
        - First, it preprocesses the data using the `filter_out_dataframe` method.
        - Then, it fits a KMeans model on the processed data.
        - Returns the trained model, predicted labels, and centroids of the clusters.
        
        Returns:
        model (KMeans): The trained KMeans model.
        labels (np.ndarray): The predicted cluster labels for each data point.
        centroids (np.ndarray): The coordinates of the centroids of the clusters.
        """
        kmeans = KMeans(n_clusters=self.number_of_clusters,
                        random_state=self.random_state)
        X_final = self.filter_out_dataframe()

        model = kmeans.fit(X=X_final)
        labels = model.predict(X_final)
        centroids = model.cluster_centers_

        return model, labels, centroids
