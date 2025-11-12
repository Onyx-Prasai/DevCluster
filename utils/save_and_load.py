import joblib
import os
from sklearn.cluster import KMeans
from typing import Optional

class SaveAndLoad:
    """
    A class to handle saving and loading of a KMeans model using joblib.
    
    The default directory for saving and loading models is '../models/'.

    """
    
    DEFAULT_PATH = "models/"
    
    def __init__(self):
        if not os.path.exists(self.DEFAULT_PATH):
            os.makedirs(self.DEFAULT_PATH)
    
    def save_model(self, model: KMeans, filename: str = 'kmeans_model.joblib') -> None:
        """
        Saves the provided KMeans model to a file in the default directory using joblib.

        Args:
            model (KMeans): The KMeans model to be saved.
            filename (str, optional): The name of the file where the model will be saved.
                                      Defaults to 'kmeans_model.joblib'.

        Returns:
            None
        """
        try:
            file_path = os.path.join(self.DEFAULT_PATH, filename)
            joblib.dump(model, file_path)
            print(f"Model saved to {file_path}")
        except Exception as e:
            print(f"An error occurred while saving the model: {e}")

    def load_model(self, filename: str = 'kmeans_model.joblib') -> Optional[KMeans]:
        """
        Loads and returns a KMeans model from the specified file in the default directory.

        Args:
            filename (str, optional): The name of the file where the model is saved.
                                      Defaults to 'kmeans_model.joblib'.

        Returns:
            KMeans: The loaded KMeans model if the file exists.
            None: If the file doesn't exist or can't be loaded.
        """
        try:
            file_path = os.path.join(self.DEFAULT_PATH, filename)
            model = joblib.load(file_path)
            print(f"Model loaded from {file_path}")
            return model
        except Exception as e:
            print(f"An error occurred while loading the model: {e}")
            return None
