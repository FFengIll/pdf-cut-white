import sys

from pdf_white_cut.logger import logger
from pdf_white_cut.util import get_parser
from pdf_white_cut.worker import batch_cut_pdf, cut_pdf

if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    if args.verbose:
        logger.remove()
        logger.add(sys.stderr, level="DEBUG")

    try:
        if args.input and args.output:
            cut_pdf(args.input, args.output, args.ignore)
        elif args.indir and args.outdir:
            batch_cut_pdf(args.indir, args.outdir, args.ignore)
        else:
            get_parser().print_help()
    except:
        exit(1)
