import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_collection import GitHubDataExtractor
from dotenv import load_dotenv

load_dotenv()

gh_token = os.getenv("GITHUB_API_TOKEN")

username = "KhagendraN"

file_path = "/home/khagendra/Projects/python/Dev/data/raw"

final_path = os.path.join(file_path, f"{username}.json")

gh_extractor = GitHubDataExtractor(username=username,
                                   token=gh_token,
                                   output_file=final_path)

print("Extracting details.. please wait..")
gh_extractor.save_raw_data()