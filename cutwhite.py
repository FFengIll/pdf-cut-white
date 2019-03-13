import argparse
import miner
import os
import sys
import logging

import PyPDF2 as pdflib
from PyPDF2 import PdfFileWriter, PdfFileReader

logging.basicConfig(
    level=logging.INFO,
    # format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    format='%(asctime)s %(filename)s[%(lineno)d] %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    # filename='parser_result.log',
    # filemode='w'
)

logger = logging.getLogger('cutwhite')
logger.setLevel(logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument("-i", help="input file", action="store",
                    default='', type=str, dest="input")
parser.add_argument("-o", help="output file", action="store",
                    default='', type=str, dest="output")
parser.add_argument("-id", help="input directory", action="store",
                    default='', type=str, dest="indir")
parser.add_argument("-od", help="output directory", action="store",
                    default='', type=str, dest="outdir")
parser.add_argument("-t", "--test", help="run test",
                    action="store_true", dest="test")
parser.add_argument("--ignore", help="ignore global",
                    action="store", type=int, default=0, dest="ignore")
parser.add_argument("--verbose", help="choose verbose (DEBUG)",
                    action="store_true", default=False, dest="verbose")
# parser.add_argument(nargs=argparse.REMAINDER, dest="value")
args = parser.parse_args()


def fix_box(page, fix):
    """
    cut the box by setting new position (relative position)
    """
    box = page.mediaBox
    logger.info(page.mediaBox)
    logger.debug(page.trimBox)
    logger.debug(page.artBox)
    logger.debug(page.cropBox)
    logger.debug(page.bleedBox)

    # must translate relative position to absolute position
    # box position
    bx, by = box.getLowerLeft()
    bx = float(bx)
    by = float(by)
    bx2, by2 = box.getUpperRight()
    bx2, by2 = float(bx2), float(by2)

    # given position to fix
    (x1, y1, x2, y2) = fix
    # FIXME: fixed position, choose the smaller area
    fx1, fy1, fx2, fy2 = max(bx, x1+bx), max(by, y1 +
                                             by), min(bx2, x2+bx), min(by2, y2+by)

    logger.info("origin box: {}".format(box))

    box.lowerLeft = (fx1, fy1)
    box.upperRight = (fx2, fy2)

    logger.info("fixed box: {}".format(box))


def cut_white(inpath, outpath='output.pdf', ignore=0):
    """
    cut the white slide of the input pdf file, and output a new pdf file.
    """
    if inpath == outpath:
        raise Exception('input and output can not be the same!')

    pages = []
    with open(inpath, 'rb') as infd:
        outpdf = PdfFileWriter()
        inpdf = PdfFileReader(infd)

        # get the visible area of the page, aka the box scale. res=[(x1,y1,x2,y2)]
        pageboxlist = miner.mine_area(inpath, ignore=ignore)

        num = inpdf.getNumPages()
        for i in range(num):
            # scale is the max box of the page
            scale = pageboxlist[i]
            page = inpdf.getPage(i)

            logger.info(scale)

            fix_box(page, scale)
            outpdf.addPage(page)

        if outpath:
            with open(outpath, 'wb') as outfd:
                outpdf.write(outfd)


def scan_files(folder, prefix=None, postfix=None, sub=False):
    """
    scan files under the dir with spec prefix and postfix
    """
    files = []

    for item in os.listdir(folder):
        path = os.path.join(folder, item)
        if os.path.isfile(path):
            if postfix:
                if item.endswith(postfix):
                    files.append(item)

    return files


def batch(indir, outdir, ignore=0):
    if indir == outdir:
        raise Exception('input and output can not be the same!')

    files = scan_files(indir, postfix='pdf')
    logger.info(files)

    if not os.path.exists(indir):
        os.mkdir(indir)

    for item in files:
        inpath = os.path.join(indir, item)
        outpath = os.path.join(outdir, item)
        cut_white(inpath, outpath, ignore=ignore)


def test_one():
    inputfile = './input/input.pdf'
    outputfile = './output/output.pdf'
    cut_white(inputfile, outputfile)


def test_batch():
    outdir = './output'
    indir = './input'
    batch(indir, outdir)


def run_tests():
    test_one()
    test_batch()


if __name__ == "__main__":
    if args.verbose:
        logging.getLogger().level = logging.DEBUG
    if args.input and args.output:
        cut_white(args.input, args.output, args.ignore)
    elif args.input:
        cut_white(args.input, None, args.ignore)
    elif args.indir and args.outdir:
        batch(args.indir, args.outdir, args.ignore)
    elif args.test:
        run_tests()
    else:
        parser.print_help()
