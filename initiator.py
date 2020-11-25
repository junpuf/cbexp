import os
import sys
import boto3


def start_build(project_name, source_version, env_overrides):
    """Doc: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client.start_build
    """
    try:
        codebuild = boto3.client("codebuild")
        response = codebuild.start_build(
            projectName=project_name,
            environmentVariablesOverride=env_overrides,
            sourceVersion=source_version,
        )
    except:
        raise
    return response


def main():
    source_version = os.getenv("CODEBUILD_RESOLVED_SOURCE_VERSION")
    webhook_trigger = os.getenv("CODEBUILD_WEBHOOK_TRIGGER")
    github_pull_number = webhook_trigger.replace("pr/", "")

    tmp_dir = "${CODEBUILD_SRC_DIR}/.tmp"
    codebuild_id = os.getenv("CODEBUILD_LOG_PATH")
    log_filename = f"build_{codebuild_id}.log"
    s3_log_uri = os.getenv("JUNPU_S3_LOG_URI")
    build_report_filepath = f"{tmp_dir}/build_report.json"
    log_filepath = f"{tmp_dir}/{log_filename}"
    s3_log_path = f"{s3_log_uri}{log_filename}" 
    build_commands = f"python3 run.py --tmp-dir {tmp_dir} --log-filename {log_filename} --build-report-filepath {build_report_filepath}"
    build_finally = [
        f"aws s3 cp {log_filepath} {s3_log_uri}",
        f"python3 comment.py --comment '`aws s3 cp {s3_log_path} .`'"
    ]
    start_build(project_name="cbexp", source_version=source_version, env_overrides=[
        {"name": "GITHUB_PULL_NUMBER", "value": github_pull_number, "type": "PLAINTEXT"},
        {"name": "GITHUB_CIMMIT_SHA", "value": source_version, "type": "PLAINTEXT"},
        {"name": "JUNPU_BUILD_COMMANDS", "value": build_commands, "type": "PLAINTEXT"},
        {"name": "JUNPU_BUILD_FINALLY", "value": "; ".join(build_finally), "type": "PLAINTEXT"}
    ])


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass