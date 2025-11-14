import requests
import json
import datetime
import time
import os

class GitHubDataExtractor:
    def __init__(self, 
                 username: str, 
                 token: str = None, 
                 output_file: str = "github_data.json", 
                 retries: int = 3, 
                 backoff_factor: float = 1.0):
        self.username = username
        self.token = token
        self.base_url = "https://api.github.com"
        self.output_file = output_file
        self.retries = retries
        self.backoff_factor = backoff_factor
        self.session = requests.Session()
        
        if self.token:
            self.session.headers.update({"Authorization": f"token {self.token}"})

    def _get(self, url, params=None):
        """Helper method to send a GET request and return the JSON response,
        with retries and pagination handling.
        """
        headers = {"Accept": "application/vnd.github.v3+json"}
        attempt = 0
        while attempt < self.retries:
            try:
                response = self.session.get(url, params=params, headers=headers)
                response.raise_for_status()  

                if response.status_code == 403 and 'X-RateLimit-Remaining' in response.headers and int(response.headers['X-RateLimit-Remaining']) == 0:
                    reset_time = int(response.headers.get('X-RateLimit-Reset', time.time()))
                    wait_time = max(0, reset_time - int(time.time()))
                    print(f"Rate limit exceeded. Sleeping for {wait_time} seconds.")
                    time.sleep(wait_time + 5)  
                    continue

                return response.json()
            
            except requests.RequestException as e:
                attempt += 1
                print(f"Attempt {attempt}/{self.retries} failed: {e}")
                if attempt < self.retries:
                    sleep_time = self.backoff_factor * (2 ** (attempt - 1))  
                    print(f"Retrying in {sleep_time} seconds...")
                    time.sleep(sleep_time)
                else:
                    print("Max retries reached. Returning None.")
                    return None

    def _fetch_paginated_data(self, url, params=None):
        """Fetch paginated data from GitHub API."""
        data = []
        page = 1
        while True:
            params = params or {}
            params['page'] = page
            response_data = self._get(url, params=params)
            if not response_data:
                break

            data.extend(response_data)
            if len(response_data) < 30:  
                break

            page += 1
        return data

    def fetch_user_data(self):
        """Fetch basic user data (followers, following, etc.)"""
        url = f"{self.base_url}/users/{self.username}"
        return self._get(url)

    def fetch_repos_data(self):
        """Fetch repository data (public repos, stars, forks, etc.)"""
        url = f"{self.base_url}/users/{self.username}/repos?type=all"
        return self._fetch_paginated_data(url)

    def fetch_pull_requests_data(self, repo_name):
        """Fetch pull requests data for a specific repository"""
        url = f"{self.base_url}/repos/{self.username}/{repo_name}/pulls?state=closed"
        return self._fetch_paginated_data(url)

    def fetch_issues_data(self, repo_name):
        """Fetch issues for a specific repository"""
        url = f"{self.base_url}/repos/{self.username}/{repo_name}/issues"
        return self._fetch_paginated_data(url)

    def fetch_commits_data(self, repo_name, since_date):
        """Fetch commits made by the user in a specific repo since a given date"""
        url = f"{self.base_url}/repos/{self.username}/{repo_name}/commits"
        params = {"since": since_date}
        return self._fetch_paginated_data(url, params)

    def fetch_repo_contents(self, repo_name):
        """Fetch the contents of a repository to check for README presence"""
        url = f"{self.base_url}/repos/{self.username}/{repo_name}/contents/"
        return self._get(url)

    def save_raw_data(self, since_days=180):
        """Fetch and save all raw data into a JSON file"""
        # Fetch user data
        user_data = self.fetch_user_data()
        if not user_data:
            return
        
        # Fetch repositories data
        repos_data = self.fetch_repos_data()
        if not repos_data:
            return

        # Prepare a dictionary to hold the raw data
        raw_data = {
            "user_data": user_data,
            "repos_data": repos_data,
            "repos_pull_requests": {},
            "repos_commits": {},
            "repos_issues": {},
            "repos_contents": {}
        }

        # Calculate date for commits (since `since_days` ago)
        since_date = (datetime.datetime.now() - datetime.timedelta(days=since_days)).isoformat()

        # For each repository, fetch pull requests, commits, issues, and contents (for README)
        for repo in repos_data:
            repo_name = repo['name']

            # Fetch Pull Requests
            pull_requests = self.fetch_pull_requests_data(repo_name)
            raw_data["repos_pull_requests"][repo_name] = pull_requests

            # Fetch Commits
            commits = self.fetch_commits_data(repo_name, since_date)
            raw_data["repos_commits"][repo_name] = commits

            # Fetch Issues
            issues = self.fetch_issues_data(repo_name)
            raw_data["repos_issues"][repo_name] = issues

            # Fetch Repository Contents (for README)
            contents = self.fetch_repo_contents(repo_name)
            raw_data["repos_contents"][repo_name] = contents

        # Save the raw data to a JSON file
        with open(self.output_file, "w") as outfile:
            json.dump(raw_data, outfile, indent=4)

        print(f"Raw data saved to {self.output_file}")

