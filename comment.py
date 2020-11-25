import os
import sys
import json
import argparse
import boto3
import requests

from github_api_v3_data_models import PullRequest


GITHUB_API_URL = "https://api.github.com"
USER = "junpuf"
REPO = "cbexp"


def main():
    pull_number = os.getenv("GITHUB_PULL_NUMBER")
    commit_sha = os.getenv("GITHUB_CIMMIT_SHA")
    args = parse_args()
    if args.comment:
        response = get_pull_request(pull_number)
        pr = PullRequest(**response.json())
        create_issue_comment(pr, args.comment, commit_sha)


def get_pull_request(pull_number):
    """Get a pull request by pull_number using GitHub REST API v3
    Endpoint Doc: https://docs.github.com/en/free-pro-team@latest/rest/reference/pulls#get-a-pull-request
    """
    arguments = {
        "url": f"{GITHUB_API_URL}/repos/{USER}/{REPO}/pulls/{pull_number}",
        "headers": {
            "authorization": get_github_access_token(),
            "accept": "application/vnd.github.v3+json"
        }
    }
    response = requests.get(**arguments)
    response.raise_for_status()
    return response


def create_issue_comment(pr, body, commit_sha):
    """Create an issue comment using GitHub REST API v3
    Endpoint Doc: https://docs.github.com/en/free-pro-team@latest/rest/reference/issues#create-an-issue-comment
    """
    headers = {
        "Authorization": get_github_access_token()
    }
    commit_page_url = f"{pr.html_url}/commits/{commit_sha}"
    text = f"""
__Commit:__ [{commit_sha}]({commit_page_url})
__Log:__ {body}
    """
    data = {
        "body": text
    }
    response = requests.post(pr.comments_url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    return response
    

def get_github_access_token():
    ACCESS_TOKEN = "junpu-github-access-token"
    return f"token {get_secrete_value(ACCESS_TOKEN)}"


def get_secrete_value(secret_id):
    secretsmanager = boto3.client("secretsmanager")
    try:
        response = secretsmanager.get_secret_value(SecretId=secret_id)
    except:
        raise
    return response["SecretString"]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--comment",
        type=str,
        required=False,
    )
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass