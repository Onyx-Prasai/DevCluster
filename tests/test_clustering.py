import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from training import Clustering
from utils import SaveAndLoad
import pandas as pd

file_path = "data/processed/synthetic.csv"

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

df = pd.read_csv(filepath_or_buffer=file_path)
kmeans_clustering = Clustering(data=df,
                               selected_features=selected_features,
                               number_of_clusters=5,
                               random_state=42)

model, labels, centroids = kmeans_clustering.fit()
print(f"Labels : {labels}")
print(f"Centroids : {centroids}")
print("Working fine!")

save_and_load = SaveAndLoad()

save_and_load.save_model(model=model)
print("Saved!")