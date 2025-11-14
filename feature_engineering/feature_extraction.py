import json

class FeatureExtractor:
    def __init__(self, data: dict):
        """
        Initializes the FeatureExtractor with the given data dictionary.
        
        :param data: The data to use for feature extraction, already loaded as a dictionary.
        """
        self.data = data  
        
    def extract_forked_repo_count(self) -> int:
        """
        Extracts the number of forked repositories from the data.

        :return: Number of forked repositories.
        """
        count = 0
        for repo in self.data["repos_data"]:
            if repo.get("fork") is True:
                count += 1
        return count
    
    def extract_total_commits(self) -> int:
        """
        Extracts the total number of commits across all repositories.

        :return: Total number of commits in the repositories.
        """
        total_commits = 0
        for commits in self.data["repos_commits"].values():
            total_commits += len(commits)  
        return total_commits
    
    def extract_total_stars(self) -> int:
        """
        Extracts the total number of stars across all repositories.

        :return: Total number of stars in the repositories.
        """
        total_stars = 0
        for repo in self.data["repos_data"]:
            stargers_count = repo.get("stargazers_count", 0)
            total_stars += stargers_count
        return total_stars
    
    def extract_pr_merged(self) -> int:
        """
        Extracts the total number of merged pull requests across all repositories.

        :return: Total number of merged pull requests.
        """
        total_prs = 0
        for repo_name, prs in self.data["repos_pull_requests"].items():
            total_prs = sum(len(prs) for prs in self.data["repos_pull_requests"].values())
        return total_prs
    
    def extract_pr_opened(self) -> int:
        """
        Extracts the total number of pull requests opened by the user across all repositories.

        :return: Total number of pull requests opened by the user.
        """
        user_login = self.data.get("user_data", {}).get("login")
        pull_requests_opened = 0
        for repo_name, prs in self.data.get("repos_pull_requests", {}).items():
            for pr in prs or []:
                if pr.get("user", {}).get("login") == user_login:
                    pull_requests_opened += 1
        return pull_requests_opened
    
    def extract_issues_count(self) -> int:
        """
        Extracts the total number of issues opened by the user across all repositories.

        :return: Total number of issues opened by the user.
        """
        user_login = self.data.get("user_data", {}).get("login")
        issues_opened = 0
        for repo_name, issues in self.data.get("repos_issues", {}).items():
            for issue in issues or []:
                if issue.get("pull_request"):
                    continue
                if issue.get("user", {}).get("login") == user_login:
                    issues_opened += 1
        return issues_opened
    
    def extract_readme_presence(self) -> float:
        """
        Extracts the ratio of repositories with a README file present.

        :return: Ratio of repositories that contain a README file.
        """
        readme_count = 0
        for repo_name, contents in self.data.get("repos_contents", {}).items():
            contents = contents or []
            has_readme = any(
                (item.get("type") == "file" and item.get("name", "").lower().startswith("readme"))
                for item in contents
            )
            if has_readme:
                readme_count += 1

        public_repo_count = len(self.data.get("repos_data", []))
        readme_presence_ratio = (readme_count / public_repo_count) if public_repo_count else 0.0
        return readme_presence_ratio

    def extract_avg_stars_per_repo(self) -> float:
        """
        Extracts the average number of stars per public repository.

        :return: Average number of stars per public repository.
        """
        public_repos = len(self.data.get("repos_data", []))
        total_stars = self.extract_total_stars()
        avg_stars = total_stars / public_repos if public_repos > 0 else 0.0
        return avg_stars

    def extract_features(self) -> dict:
        """
        Extracts all the relevant features for the user from the given data.

        :return: A dictionary containing all the extracted features.
        """
        public_repos = len(self.data["repos_data"])

        forked_repo_count = self.extract_forked_repo_count()
        forked_repo_ratio = forked_repo_count / public_repos if public_repos > 0 else 0

        commit_count_last_6m = self.extract_total_commits()
        stars_total = self.extract_total_stars()
        pull_requests_merged = self.extract_pr_merged()
        pull_requests_opened = self.extract_pr_opened()
        issues_opened = self.extract_issues_count()
        readme_presence_ratio = self.extract_readme_presence()
        avg_stars_per_repo = self.extract_avg_stars_per_repo()

        followers = self.data["user_data"]["followers"]
        following = self.data["user_data"]["following"]

        features = {
            "public_repos": public_repos,
            "forked_repo_ratio": forked_repo_ratio,
            "commit_count_last_6m": commit_count_last_6m,
            "stars_total": stars_total,
            "followers": followers,
            "pull_requests_merged": pull_requests_merged,
            "avg_stars_per_repo": avg_stars_per_repo,
            "following": following,
            "pull_requests_opened": pull_requests_opened,
            "issues_opened": issues_opened,
            "readme_presence_ratio": readme_presence_ratio,
        }
        
        return features
    
def open_raw_file(file_path: str=None) -> dict:
    with open(file_path, "r") as f:
        data = json.load(f)
    return data




