import argparse
import sys

from pdf_white_cut import parse_args, logger
from pdf_white_cut.cutter import  cut_pdf, batch_cut_pdf
from pdf_white_cut.test import tests

if __name__ == "__main__":
    args = parse_args()
    if args.verbose:
        logger.remove()
        logger.add(sys.stderr, level="DEBUG")

    if args.input and args.output:
        cut_pdf(args.input, args.output, args.ignore)
    elif args.input:
        cut_pdf(args.input, None, args.ignore)
    elif args.indir and args.outdir:
        batch_cut_pdf(args.indir, args.outdir, args.ignore)
    elif args.test:
        tests()
