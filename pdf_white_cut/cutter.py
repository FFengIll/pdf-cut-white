import os
import sys

import loguru
from PyPDF2 import PdfFileWriter, PdfFileReader
from path import Path

from pdf_white_cut import analyzer

logger = loguru.logger


def edit_box(page, useful_area):
    """
    cut the box by setting new position (relative position)
    """
    box = page.mediaBox
    # MENTION: media box is a visible area of the pdf page
    logger.info("media box: {}", page.mediaBox)
    logger.info("trim box: {}", page.trimBox)
    logger.info("art box: {}", page.artBox)
    logger.info("crop box: {}", page.cropBox)
    logger.info("bleed box: {}", page.bleedBox)

    # must translate relative position to absolute position
    # box position
    bx1, by1 = box.getLowerLeft()
    bx1, by1 = float(bx1), float(by1)
    bx2, by2 = box.getUpperRight()
    bx2, by2 = float(bx2), float(by2)

    # visible area
    (x1, y1, x2, y2) = useful_area

    # MENTION: all of the box is relative position, so we need to fix the position, choose the smaller area
    logger.info("origin box: {}", box)

    box.lowerLeft = (max(bx1, x1 + bx1), max(by1, y1 + by1))
    box.upperRight = (min(bx2, x2 + bx1), min(by2, y2 + by1))

    logger.info("fixed box: {}", box)


def cut_pdf(source, target: str = None, ignore=0):
    """
    cut the white slide of the input pdf file, and output a new pdf file.
    """
    if target is None:
        target = "output.pdf"

    if source == target:
        logger.error("{} {}", source, target)
        raise Exception("input and output can not be the same!")

    try:
        with open(source, "rb") as infd:
            logger.info("process file: {}", source)
            inpdf = PdfFileReader(infd)

            # MENTION: never move and change the sequence, since file IO
            # get the visible area of the page, aka the box scale. res=[(x1,y1,x2,y2)]
            page_box_list = analyzer.analyse_area(source, ignore=ignore)
            outpdf = PdfFileWriter()

            for idx in range(inpdf.getNumPages()):
                # scale is the max box of the page
                scale = page_box_list[idx]
                logger.info("origin scale: {}", scale)

                page = inpdf.getPage(idx)
                edit_box(page, scale)
                outpdf.addPage(page)

            with open(target, "wb") as outfd:
                outpdf.write(outfd)
                logger.info("output file: {}", target)

    except UnicodeEncodeError as ue:
        logger.exception("UnicodeEncodeError while processing file:{}", source)
        logger.exception(ue)
    except Exception as e:
        logger.exception("Some other Error while processing file:{}", source)
        logger.exception(e)


def scan_files(folder, glob=""):
    """
    scan files under the dir with spec prefix and postfix
    """
    files = []
    for item in Path(folder).listdir(glob):
        item: "Path"
        files.append(item.basename())
    return files


def batch_cut_pdf(indir, outdir, ignore=0):
    if indir == outdir:
        raise Exception("input and output can not be the same!")

    files = scan_files(indir, glob="*.pdf")
    logger.info(files)

    if not os.path.exists(indir):
        os.mkdir(indir)

    logger.info("input dir: {}", indir)
    logger.info("output dir: {}", outdir)
    for item in files:
        source = Path.joinpath(indir, item)
        target = Path.joinpath(outdir, item)
        logger.info("{} {} ", source, target)
        cut_pdf(source, target, ignore=ignore)
