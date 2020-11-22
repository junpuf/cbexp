import logging
import sys
import argparse
import os

def main():
    args = parse_args()
    if os.path.exists(args.log_filepath):
        os.remove(args.log_filepath)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(message)s')
    # file logging
    logfile_handler = logging.FileHandler(args.log_filepath)
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

    # log some stuff
    for i in range(1000):
        logger.warning("hello world")


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
        sys.exit(main())
    except KeyboardInterrupt:
        pass