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
    build_commands = "python3 run.py --log-filepath \"${CODEBUILD_SRC_DIR}/.tmp/build_${CODEBUILD_LOG_PATH}.log\""
    build_finally = "aws s3 cp ${CODEBUILD_SRC_DIR}/.tmp/build_${CODEBUILD_LOG_PATH}.log ${JUNPU_S3_LOG_URI}"    
    start_build(project_name="cbexp", source_version=source_version, env_overrides=[
        {"name": "JUNPU_BUILD_COMMANDS", "value": build_commands, "type": "PLAINTEXT"},
        {"name": "JUNPU_BUILD_FINALLY", "value": build_finally, "type": "PLAINTEXT"}
    ])


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass