import argparse
from pdf_white_cut.logger import logger


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", help="input file", action="store", default="", type=str, dest="input"
    )
    parser.add_argument(
        "-o",
        help="output file (DEFAULT: output.pdf)",
        action="store",
        default="output.pdf",
        type=str,
        dest="output",
    )
    parser.add_argument(
        "-id",
        help="input directory",
        action="store",
        default=".",
        type=str,
        dest="indir",
    )
    parser.add_argument(
        "-od",
        help="output directory",
        action="store",
        default=".",
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
        help="verbose (DEBUG)",
        action="store_true",
        default=False,
        dest="verbose",
    )
    return parser
