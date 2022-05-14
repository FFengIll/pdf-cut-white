import argparse
import sys

import loguru

logger = loguru.logger
logger.remove()
logger.add(sys.stderr, level="INFO")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", help="input file", action="store", default="", type=str, dest="input"
    )
    parser.add_argument(
        "-o", help="output file", action="store", default="", type=str, dest="output"
    )
    parser.add_argument(
        "-id",
        help="input directory",
        action="store",
        default="",
        type=str,
        dest="indir",
    )
    parser.add_argument(
        "-od",
        help="output directory",
        action="store",
        default="",
        type=str,
        dest="outdir",
    )
    parser.add_argument(
        "-t", "--test", help="run test", action="store_true", dest="test"
    )
    parser.add_argument(
        "--ignore",
        help="ignore global",
        action="store",
        type=int,
        default=0,
        dest="ignore",
    )
    parser.add_argument(
        "--verbose",
        help="choose verbose (DEBUG)",
        action="store_true",
        default=False,
        dest="verbose",
    )
    # parser.add_argument(nargs=argparse.REMAINDER, dest="value")
    args = parser.parse_args()
    return args
