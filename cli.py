import sys

from pdf_white_cut.cutter import batch_edit_pdf, edit_pdf
from pdf_white_cut.logger import logger
from pdf_white_cut.parser import get_parser

if __name__ == "__main__":
    parser = get_parser()
    args = get_parser().parse_args()
    if args.verbose:
        logger.remove()
        logger.add(sys.stderr, level="DEBUG")

    try:
        if args.input and args.output:
            edit_pdf(args.input, args.output, args.ignore)
        elif args.indir and args.outdir:
            batch_edit_pdf(args.indir, args.outdir, args.ignore)
        else:
            get_parser().print_help()
    except:
        exit(1)
