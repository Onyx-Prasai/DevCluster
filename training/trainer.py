import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import SaveAndLoad
from clustering import Clustering
from utils import get_error_message_details
import pandas as pd
from utils import setup_logger

logger = setup_logger()

def main():
    selected_features = [
    "public_repos",
    "forked_repo_ratio",
    "commit_count_last_6m",
    "stars_total",
    "followers",
    "pull_requests_merged",
    "avg_stars_per_repo",
    "following",
    "pull_requests_opened",
    "issues_opened",
    "readme_presence_ratio",
    ]

    try:
        file_path = "data/processed/synthetic.csv"
        logger.info("Training data found!")

        df = pd.read_csv(filepath_or_buffer=file_path)
        logger.info("Training data loaded as Dataframe!")

        kmeans_clustering = Clustering(data=df,
                               selected_features=selected_features,
                               number_of_clusters=5,
                               random_state=42)
        
        logger.info("Training started..")
        model, labels, centroids = kmeans_clustering.fit()

        logger.info("Saving the model!")
        model_handler = SaveAndLoad()

        model_handler.save_model(model=model, filename="kmeans_test.joblib")
        print(f"Labels: {labels}")
        print(f"Centroids: {centroids}")

    except Exception as e:
        error_details = get_error_message_details(error=e)
        logger.warning(error_details)

if __name__ == "__main__":
    main()
    