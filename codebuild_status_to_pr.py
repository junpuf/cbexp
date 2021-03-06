import logging
import os
import sys
import argparse
from github import GitHubHandler

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(logging.StreamHandler(sys.stdout))
LOGGER.addHandler(logging.StreamHandler(sys.stderr))


def get_args():
    """
    Manage arguments to this script when called directly
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--status")
    return parser.parse_args()


def get_target_url(project):
    """
    Set the link for "Details" on PR builds

    :param project: CodeBuild project name associated with the running build
    :return: Link for the "Details" link associated with a GitHub status check
    """
    region = os.getenv("AWS_REGION")
    logpath = os.getenv("CODEBUILD_LOG_PATH")
    return (
        f"https://{region}.console.aws.amazon.com/"
        f"codesuite/codebuild/projects/{project}/build/{project}%3A{logpath}/log?region={region}"
    )


def post_status(status):
    """
    Post the codebuild status to the PR.
    """
    handler = GitHubHandler()
    codebuild_name = os.getenv("JUNPU_BUILD_NAME")
    handler.set_status(
        state=status,
        context=codebuild_name,
        description=status,
        target_url=get_target_url(codebuild_name),
    )


def main():
    args = get_args()
    codebuild_statuses = {"0": "failure", "1": "success", "2": "pending"}
    status = codebuild_statuses[args.status]
    post_status(status)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
