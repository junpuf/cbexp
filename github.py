import os
import requests
import json
from secrets_manager import SecretsManager


class GitHubHandler(object):
    """
    Methods to handle interacting with GitHub
    """

    GITHUB_API_URL = "https://api.github.com"
    OAUTH_TOKEN = "junpu-github-access-token"

    def __init__(self, user="junpuf", repo="cbexp"):
        self.user = user
        self.repo = repo
        self.commit_hash = os.getenv("CODEBUILD_RESOLVED_SOURCE_VERSION")

    def get_auth_token(self):
        """
        Args:
            None
        Return:
            str
        """
        return SecretsManager().get_secret_value(self.OAUTH_TOKEN)

    def get_authorization_header(self):
        """
        Args:
            None
        Returns:
            dict
        """
        token = self.get_auth_token()
        return {"Authorization": "token {}".format(token)}

    def set_status(self, state, **kwargs):
        """
        Args:
            state: success, failure
            **kwargs: common parameters - target_url, description, context
        Returns:
            requests object
        """
        url = f"{self.GITHUB_API_URL}/repos/{self.user}/{self.repo}/statuses/{self.commit_hash}"
        data = {"state": state}

        for key, value in kwargs.items():
            data[key] = value

        response = requests.post(
            url, headers=self.get_authorization_header(), data=json.dumps(data)
        )
        response.raise_for_status()
        return response

    def get_latest_sha(self, pull_request):
        """
        Get most recent sha from the PR

        Returns: <str> sha ID of commit
        """
        pr_details = self.get_pr_details(pull_request)
        return pr_details.json()["head"]["sha"]

    def get_pr_title(self, pull_request):
        """
        Get PR title

        Returns: <str> PR title
        """
        pr_details = self.get_pr_details(pull_request)

        return pr_details.json()["title"]

    def get_pr_body(self, pull_request):
        """
        Get PR body

        Returns: <str> PR body
        """
        pr_details = self.get_pr_details(pull_request)

        return pr_details.json()["body"]

    def get_pr_labels(self, pull_request):
        """
        Get PR labels

        Returns: <str> PR labels
        """
        pr_details = self.get_pr_details(pull_request)

        return pr_details.json()["labels"]

    def get_pr_details(self, pull_request):
        """
        Get the whole status from a given PR

        Returns: full response object from PR
        """
        url = f"{self.GITHUB_API_URL}/repos/{self.user}/{self.repo}/pulls/{pull_request}"
        response = requests.get(url, headers=self.get_authorization_header())
        response.raise_for_status()
        return response

    def get_pr_files_changed(self, pull_request):
        """
        Get the list of files changed in a PR

        Returns: List of filenames
        """

        url = f"{self.GITHUB_API_URL}/repos/{self.user}/{self.repo}/pulls/{pull_request}/files"

        response = requests.get(url, headers=self.get_authorization_header())
        response.raise_for_status()
        files_changed = json.loads(response.text)
        return [_file["filename"] for _file in files_changed]
