import os
import sys
import boto3

def start_build(project_name, source_version, env_overrides):
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
        f"python3 github_actions.py --commit_sha {source_version} --comment 'Log is located at `{s3_log_path}`, you can run `aws s3 cp {s3_log_path} .` to download it.'"
    ]
    start_build(project_name="cbexp", source_version=source_version, env_overrides=[
        {"name": "JUNPU_BUILD_COMMANDS", "value": build_commands, "type": "PLAINTEXT"},
        {"name": "JUNPU_BUILD_FINALLY", "value": "; ".join(build_finally), "type": "PLAINTEXT"}
    ])


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass