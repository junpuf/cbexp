import os
import sys
import json
import argparse
import boto3
import requests


from data_models.github_api_v3 import PullRequest


GITHUB_API_URL = "https://api.github.com"
USER = "junpuf"
REPO = "cbexp"


def main():
    args = parse_args()
    if args.comment:
        pull_requests = get_pull_requests_by_commit_sha(args.commit_sha) # assume only 1 PR has this commit_sha
        pr = PullRequest(**pull_requests.json()[0])
        create_issue_comment(pr, args.comment)


def get_pull_requests_by_commit_sha(commit_sha):
    """Create an issue comment using GitHub REST API v3
    Endpoint: GET /repos/:owner/:repo/commits/:commit_sha/pulls
    Doc: https://developer.github.com/v3/repos/commits/#list-pull-requests-associated-with-a-commit
    """
    url = f"{GITHUB_API_URL}/repos/{USER}/{REPO}/commits/{commit_sha}/pulls"
    header = {
        "Accept": "application/vnd.github.groot-preview+json",
        "Authorization": get_github_access_token()
    }
    response = requests.get(url, headers=header)
    response.raise_for_status()
    return response


def create_issue_comment(pr, body):
    """Create an issue comment using GitHub REST API v3
    Endpoint: POST /repos/:owner/:repo/issues/:issue_number/comments
    Doc: https://developer.github.com/v3/issues/comments/#create-an-issue-comment
    """
    headers = {
        "Authorization": get_github_access_token()
    }
    text = f"""
__Commit:__ [{pr.commits_url}]({pr.commits_url})
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
        "--commit_sha",
        type=str,
        default=None,
        required=True,
    )
    parser.add_argument(
        "--comment",
        type=str,
        default=None,
        required=False,
    )
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass