import logging
import sys
import argparse
import os
import json

def main():
    args = parse_args()

    # build report setup
    if os.path.exists(args.build_report_filepath):
        os.remove(args.build_report_filepath)
    with open(args.build_report_filepath, 'w') as build_report_file:
        s3_log_dir = os.getenv("JUNPU_S3_LOG_URI")
        s3_log_uri = f"{s3_log_dir}{args.log_filename}"
        build_report_data = {
            "s3_log_uri": f"{s3_log_uri}"
        }
        json.dump(build_report_data, build_report_file)
    
    # logger setup
    log_filepath = os.path.join(args.tmp_dir, args.log_filename)
    logger = get_logger(log_filepath)

    # log some stuff
    for i in range(100):
        logger.warning("hello world")


def get_logger(log_filepath):
    if os.path.exists(log_filepath):
        os.remove(log_filepath)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(message)s')
    # file logging
    logfile_handler = logging.FileHandler(log_filepath)
    logfile_handler.setFormatter(formatter)
    logger.addHandler(logfile_handler)
    # stdout logging
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)
    # stderr logging
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setFormatter(formatter)
    logger.addHandler(stderr_handler)
    return logger


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--tmp-dir",
        default=None,
        required=True,
    )
    parser.add_argument(
        "--log-filename",
        default=None,
        required=True,
    )
    parser.add_argument(
        "--build-report-filepath",
        default=None,
        required=True,
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    try:
        root = os.getenv("CODEBUILD_SRC_DIR")
        tmp_dir = os.path.join(root, ".tmp") 
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)        
        sys.exit(main())
    except KeyboardInterrupt:
        pass