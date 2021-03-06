import os
import sys
import boto3


def start_build(project_name, source_version, buildspec, env_overrides):
    """Doc: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.start_build
    """
    try:
        codebuild = boto3.client("codebuild")
        response = codebuild.start_build(
            projectName=project_name,
            sourceVersion=source_version,
            buildspecOverride=buildspec,
            environmentVariablesOverride=env_overrides,
        )
    except:
        raise
    return response


def main():
    source_version = os.getenv("CODEBUILD_RESOLVED_SOURCE_VERSION")
    webhook_trigger = os.getenv("CODEBUILD_WEBHOOK_TRIGGER")
    github_pull_number = webhook_trigger.replace("pr/", "")

    for i in range(10):
        start_build(project_name="cbexp", source_version=source_version, buildspec="build.yml", env_overrides=[
            {"name": "GITHUB_PULL_NUMBER", "value": github_pull_number, "type": "PLAINTEXT"},
            {"name": "GITHUB_CIMMIT_SHA", "value": source_version, "type": "PLAINTEXT"},
            {"name": "JUNPU_BUILD_NAME", "value": f"junpu-cbexp-{i}", "type": "PLAINTEXT"}
        ])


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass