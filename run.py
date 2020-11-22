import logging
import sys
import argparse
import os

def main():
    args = parse_args()
    logger = get_logger(args.log_filepath)

    # log some stuff
    for i in range(1000):
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
        "--log-filepath",
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