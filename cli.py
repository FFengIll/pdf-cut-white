import sys

from pdf_white_cut.cutwhite import parse_args, logger, cut_white, batch
from pdf_white_cut.test import tests

if __name__ == "__main__":
    args = parse_args()
    if args.verbose:
        logger.remove()
        logger.add(sys.stderr, level="DEBUG")

    if args.input and args.output:
        cut_white(args.input, args.output, args.ignore)
    elif args.input:
        cut_white(args.input, None, args.ignore)
    elif args.indir and args.outdir:
        batch(args.indir, args.outdir, args.ignore)
    elif args.test:
        tests()
