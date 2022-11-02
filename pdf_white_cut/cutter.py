import os

from PyPDF2 import PdfWriter, PdfReader
from path import Path

from pdf_white_cut import analyzer
from pdf_white_cut.logger import logger


def edit_page_box(page, visible_box):
    """
    cut the box by setting new position (relative position)
    """
    box = page.mediabox
    # MENTION: media box is a visible area of the pdf page
    logger.info("media box: {}", page.mediabox)
    logger.info("trim box: {}", page.trimbox)
    logger.info("art box: {}", page.artbox)
    logger.info("crop box: {}", page.cropbox)
    logger.info("bleed box: {}", page.bleedbox)

    # must translate relative position to absolute position
    # box position
    bx1, by1, bx2, by2 = [
        float(i) for i in list(box.lower_left) + list(box.upper_right)
    ]

    # visible area
    x1, y1, x2, y2 = [float(i) for i in visible_box]

    # MENTION: all boxes is relative position, so we need to fix the position, choose the smaller area
    logger.info("origin media box: {}", box)

    box.lower_left = (max(bx1, x1 + bx1), max(by1, y1 + by1))
    box.upper_right = (min(bx2, x2 + bx1), min(by2, y2 + by1))

    logger.info("cut media box to: {}", box)


def edit_pdf(source: str, target: str, ignore=0):
    """
    edit to cut the white slide of the input pdf file, and output a new pdf file.
    """
    if source == target:
        logger.error("{} {}", source, target)
        raise Exception("input and output can not be the same!")

    try:
        # MENTION: never move and change the sequence, since file IO.
        # analyses the visible box of each page, aka the box scale. res=[(x1,y1,x2,y2)]
        # analyses whole pdf at one time since it use `pdfminer` (not `PyPDF2`)
        page_box_list = analyzer.extract_pdf_boxs(source, ignore=ignore)

        # edit pdf by visible box and output it
        with open(source, "rb") as infd:
            logger.info("input file: {}", source)
            inpdf = PdfReader(infd)
            outpdf = PdfWriter()

            for idx, page in enumerate(inpdf.pages):
                # scale is the max box of the page
                box = page_box_list[idx]
                logger.info("origin scale: {}", box)

                page = inpdf.pages[idx]
                edit_page_box(page, box)
                outpdf.add_page(page)

            Path(target).dirname().makedirs_p()
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


def batch_edit_pdf(indir, outdir, ignore=0):
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
        edit_pdf(source, target, ignore=ignore)
