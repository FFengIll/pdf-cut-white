import sys

from pdf_white_cut import parse_args, logger, get_parser
from pdf_white_cut.cutter import cut_pdf, batch_cut_pdf

if __name__ == "__main__":
    args = parse_args()
    if args.verbose:
        logger.remove()
        logger.add(sys.stderr, level="DEBUG")

    if args.input and args.output:
        cut_pdf(args.input, args.output, args.ignore)
    elif args.indir and args.outdir:
        batch_cut_pdf(args.indir, args.outdir, args.ignore)
    else:
        get_parser().print_help()
