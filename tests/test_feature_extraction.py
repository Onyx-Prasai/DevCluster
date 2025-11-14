import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from feature_engineering import FeatureExtractor, open_raw_file

file_path = "/home/khagendra/Projects/python/Dev/data/raw/KhagendraN.json"

if os.path.exists(file_path):
    data = open_raw_file(file_path=file_path)
    feature_extract = FeatureExtractor(data=data)
    final_data = feature_extract.extract_features()
    print(final_data)
    print("PASSED!")

else:
    print("File not found!")
