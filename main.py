import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import SimpleImputer
from feature_engineering import FeatureExtractor, open_raw_file
from data_collection import GitHubDataExtractor
from training import Scorer
from utils import (setup_logger,
                   APIError,
                   ConfigError,
                   get_error_message_details,
                   SaveAndLoad)
from dotenv import load_dotenv

logger = setup_logger()

try:
    load_dotenv()
    gh_token = os.getenv("GITHUB_API_TOKEN")
except ConfigError as e:
    logger.error(f"Config error during token extraction: {get_error_message_details(e)}")
    raise

logger = setup_logger()
interpretation = {
    0: "Cluster 0 –→ Effectively dead/noise: Accounts that are likely inactive or abandoned, with high repository counts but minimal engagement or contribution. These users have low activity and limited interaction, often creating noise without adding real value.",
    1: "Cluster 1 –→ True open-source unicorns: Highly active and influential individuals or maintainers of high-profile open-source projects. These are the niche experts and leaders driving innovation in specialized areas.",
    2: "Cluster 2 –→ Healthy mid-tier: This cluster represents consistent contributors, typically they are hobbyist groups. Their growth is steady, contributing reliably without extremes.",
    3: "Cluster 3 –→ Solid but less visible workhorses: Users who are very consistent but may not get the same level of visibility as Cluster 1 or 2. They focus on volume rather than viral reach and contribute regularly. Their work tends to be high-output but is often more internal or focused on specific areas that may not be as publicly visible.",
    4: "Cluster 4 –→ High-output professional powerhouses: This group consists of professional organizations or prolific individuals, consistently producing high-output projects that are highly impactful. They have a significant social reach, often with a larger focus on collaboration and forking. Their contributions are not just numerous but also impactful, helping drive the ecosystem forward at scale."
}

scores = {
    0: (0.0, 20.0),  
    3: (20.0, 60.0), 
    4: (40.0, 70.0), 
    2: (65.0, 85.0), 
    1: (85.0, 100.0)  
}

# Path to store raw data
file_path = "/home/khagendra/Projects/python/Dev/data/raw"

def extract_user_data(user_name: str, token: str, output_path: str) -> None:
    """
    Extracts raw GitHub user data and saves it to the specified path.

    Parameters:
        user_name (str): GitHub username.
        token (str): GitHub API token for authentication.
        output_path (str): Path where the raw data will be saved.
    """
    try:
        # Check if the file already exists
        if os.path.exists(output_path):
            logger.info(f"Raw data for user '{user_name}' already exists at {output_path}. Skipping data extraction.")
        else:
            logger.info(f"Extracting data for user: {user_name}")
            data_extractor = GitHubDataExtractor(username=user_name,
                                                 token=token,
                                                 output_file=output_path,
                                                 retries=2)
            data_extractor.save_raw_data(since_days=180)
            logger.info(f"GitHub data extraction complete for user: {user_name}. Data saved to {output_path}")
    except APIError as e:
        logger.error(f"API error during data extraction: {get_error_message_details(e)}")
        raise

def extract_features(file_path: str) -> pd.DataFrame:
    """
    Extract features from raw data and return a DataFrame.

    Parameters:
        file_path (str): Path to the raw data file.

    Returns:
        pd.DataFrame: DataFrame containing extracted features.
    """
    try:
        logger.info("Starting feature extraction...")
        raw_data = open_raw_file(file_path=file_path)
        feature_extractor = FeatureExtractor(data=raw_data)
        extracted_features = feature_extractor.extract_features()
        
        if not extracted_features:
            logger.error("No features extracted. The extracted features are empty.")
            raise ValueError("No features extracted.")
        
        logger.info(f"Extracted features: {extracted_features}")
        return pd.DataFrame(data=[extracted_features])
    except Exception as e:
        logger.error(f"Error during feature extraction: {str(e)}")
        raise

def preprocess_data(X: pd.DataFrame) -> np.ndarray:
    """
    Preprocesses the data by scaling and imputing missing values.

    Parameters:
        X (pd.DataFrame): DataFrame containing extracted features.

    Returns:
        np.ndarray: Preprocessed data.
    """
    # Replace infinite values with NaN
    X.replace([np.inf, -np.inf], np.nan, inplace=True)

    # Scaling the features to the range [1, 10]
    logger.info("Scaling data...")
    scaler = MinMaxScaler(feature_range=(1, 10))
    X_scaled = scaler.fit_transform(X.values)

    # Imputing missing values using median
    logger.info("Imputing missing values...")
    imputer = SimpleImputer(strategy='median')
    X_imputed = imputer.fit_transform(X_scaled)

    logger.info("Data preprocessing complete.")
    return X_imputed

def load_model() -> object:
    """
    Loads the pre-trained machine learning model.

    Returns:
        object: The loaded machine learning model.
    """
    try:
        model_handler = SaveAndLoad()
        model = model_handler.load_model()
        logger.info("Model loaded successfully.")
        return model
    except Exception as e:
        logger.error(f"Error loading the model: {str(e)}")
        raise

def make_predictions(model: object, X: np.ndarray) -> int:
    """
    Makes predictions using the loaded model.

    Parameters:
        model (object): The pre-trained model.
        X (np.ndarray): The preprocessed input data.

    Returns:
        np.ndarray: Model predictions.
    """
    try:
        logger.info("Making predictions...")
        return model.predict(X)[0]
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise

def main():
    """
    Main function to run the complete pipeline: data extraction, feature extraction,
    preprocessing, model loading, prediction, and scoring.
    """
    # User input for GitHub username
    user_name = input("Enter GitHub username: ")
    raw_data_file_path = os.path.join(file_path, f"{user_name}.json")

    # Data collection
    extract_user_data(user_name=user_name, token=gh_token, output_path=raw_data_file_path)

    # Feature extraction
    features = extract_features(file_path=raw_data_file_path)

    # Data preprocessing
    preprocessed_data = preprocess_data(features)

    # Model loading
    model = load_model()

    # Making predictions
    label = make_predictions(model, preprocessed_data)
    centroid_for_label = model.cluster_centers_[label]

    # Scoring predictions
    scorer = Scorer(label=label,
                    input_array=preprocessed_data,
                    centroid=centroid_for_label,
                    interpretation=interpretation,
                    scores=scores)
    logger.info("Calculating score!")
    interpretation_final, final_score = scorer.compute_score()
    print(f"Label : {label}")
    print(f"Score : {final_score}")
    print(f"Description: {interpretation_final}")

if __name__ == "__main__":
    main()
