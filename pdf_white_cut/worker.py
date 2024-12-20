#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy
import sys
from typing import List, Tuple

import fitz  # PyMuPDF
from path import Path
from pdfminer import layout
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import (
    LAParams,
    LTAnno,
    LTChar,
    LTContainer,
    LTCurve,
    LTFigure,
    LTImage,
    LTLine,
    LTRect,
    LTTextBox,
    LTTextLine,
)
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser

from pdf_white_cut.logger import logger


def cut_page_box(page: fitz.Page, visible_box: fitz.Rect):
    """
    cut the box by setting new position (relative position)
    """

    old_media_box = copy.deepcopy(page.mediabox)
    box = page.mediabox
    # MENTION: media box is a visible area of the pdf page
    logger.info("media box: {}", page.mediabox)
    logger.info("trim box: {}", page.trimbox)
    logger.info("art box: {}", page.artbox)
    logger.info("crop box: {}", page.cropbox)
    logger.info("bleed box: {}", page.bleedbox)

    # must translate relative position to absolute position
    # box position
    bx1, by1, bx2, by2 = [box.x0, box.y0, box.x1, box.y1]

    # visible area
    x1, y1, x2, y2 = [float(i) for i in visible_box]

    # MENTION: all boxes is relative position, so we need to fix the position, choose the smaller area
    logger.info("origin media box: {}", box)

    box.lower_left = (max(bx1, x1 + bx1), max(by1, y1 + by1))
    box.upper_right = (min(bx2, x2 + bx1), min(by2, y2 + by1))

    logger.info("cut media box to: {}", box)

    # Define a new MediaBox (left, bottom, right, top)
    # This example reduces each side by 10 units
    new_media_box = fitz.Rect(*box.lower_left, *box.upper_right)

    # Set the new MediaBox for the page
    page.set_mediabox(new_media_box)
    #
    # now we know if it changed
    changed = old_media_box != new_media_box

    logger.info(
        "pdf bbox changed: {} ({} {})",
        changed,
        new_media_box,
        old_media_box,
    )
    return changed


def cut_pdf(source: Path, target: Path, ignore=0):
    """
    edit to cut the white slide of the input pdf file, and output a new pdf file.
    """
    # guard type
    source = Path(source)
    target = Path(target)

    if source == target:
        logger.error("{} {}", source, target)
        raise Exception("input and output can not be the same!")

    if not source.exists():
        raise Exception("input file not exists! ({})".format(source))

    # make dir if possible
    target.absolute().dirname().makedirs_p()

    try:
        # edit pdf by visible box and output it
        logger.info("input file: {}", source)

        # MENTION: never move and change the sequence, since file IO.
        # analyses the visible box of each page, aka the box scale. res=[(x1,y1,x2,y2)]
        # analyses whole pdf at one time since it use `pdfminer` (not `pypdf`)
        page_box_list = extract_pdf_boxs(source, ignore=ignore)

        inpdf = fitz.open(str(source))

        for idx, page in enumerate(inpdf.pages()):
            # scale is the max box of the page
            box = page_box_list[idx]
            logger.info("origin scale: {}", box)

            cut_page_box(page, box)

        logger.info("output to {}", Path(target))

        # add some metadata
        inpdf.metadata["editor"] = "pdf-cut-white"

        inpdf.save(target, incremental=False)
        inpdf.close()

    except UnicodeEncodeError as ue:
        logger.exception("UnicodeEncodeError while processing file:{}", source)
        logger.exception(ue)
        raise ue
    except Exception as e:
        logger.exception("Some unknown Error while processing file:{}", source)
        logger.exception(e)
        raise e


def batch_cut_pdf(indir: Path, outdir: Path, ignore=0):
    # guard type
    indir = Path(indir)
    outdir = Path(outdir)

    if indir.absolute() == outdir.absolute():
        raise Exception("input and output can not be the same!")

    # make dir if possible for output
    outdir.makedirs_p()

    logger.info("input dir: {}", indir)
    logger.info("output dir: {}", outdir)

    # only get one layer of pdf files
    files = [pdf.basename() for pdf in indir.files("*.pdf")]
    logger.info("pdf files in spec folder: {}", files)

    # guard dir
    outdir.makedirs_p()

    for item in files:
        source = Path.joinpath(indir, item)
        target = Path.joinpath(outdir, item)
        logger.info("{} {} ", source, target)
        cut_pdf(source, target, ignore=ignore)


def determine_max_box(boxs: List) -> Tuple:
    down_left = [sys.maxsize, sys.maxsize]
    upper_right = [
        -sys.maxsize,
        -sys.maxsize,
    ]
    for box in boxs:
        if box is None:
            continue
        for idx, (cur, other) in enumerate(zip(down_left, box[0:2])):
            down_left[idx] = min(cur, other)
        for idx, (cur, other) in enumerate(zip(upper_right, box[2:])):
            upper_right[idx] = max(cur, other)

    return tuple(down_left) + tuple(upper_right)


def extract_item_box(item):
    """
    this is the core process logic for the tool
    which analyse all items in pdf type by type.
    """
    # no bbox for LTAnno
    if isinstance(item, LTAnno):
        return None

    # use bbox as default area
    bbox = item.bbox

    if isinstance(item, LTLine):
        logger.debug("use itself: {}", item)
    elif isinstance(item, LTRect):
        logger.debug("use itself: {}", item)
    elif isinstance(item, LTCurve):
        logger.debug("use itself: {}", item)
    elif isinstance(item, LTTextBox):
        if isinstance(item, layout.LTTextBoxHorizontal):
            ...
            logger.warning("LTTextBoxHorizontal: {}", item)
        elif isinstance(item, layout.LTTextBoxVertical):
            ...
            logger.warning("LTTextBoxVertical: {}", item)
        else:
            logger.warning("use itself since NotImplemented: {}", item)
    elif isinstance(item, LTTextLine):
        # there is 2 types of `LTTextLine`: horizontal and vertical
        text = item.get_text().encode("unicode_escape")
        logger.debug("analyse LTTextLine: {} {}", item, text)
        # TODO: here we ignored fonts and text line direction, may error in some cases
        # since the text has a height on y-axis, or has a width on x-axis,
        # we must modify it to make the whole text visible
        # FIXME: now we use `half` for upper and lower, may not right but work
        bbox = (
            bbox[0] - item.width / 2,
            bbox[1] - item.height / 2,
            bbox[2] + item.width / 2,
            bbox[3] + item.height / 2,
        )
        return bbox

        # might check chart one by one
        # children_bbox = [extract_box(ch) for ch in item]
        # return get_max_box(children_bbox)
    elif isinstance(item, LTChar):
        text = item.get_text().encode("unicode_escape")
        logger.debug("analyse LTChar: {} {}", item, text)
        bbox = (
            bbox[0] - item.width / 2,
            bbox[1] - item.height / 2,
            bbox[2] + item.width / 2,
            bbox[3] + item.height / 2,
        )
    elif isinstance(item, LTImage):
        logger.warning("use itself since NotImplemented: {}", item)
    elif isinstance(item, LTFigure):
        logger.debug("analyse LTFigure:{}", item)
        # for `LTFigure`, the bbox is modified in `PDFMiner`
        # we should use the content item inside it to calculate real result
        try:
            children_bbox = []
            # _objs is the original items, of course, only one item for `LTFigure`
            for subfigure in item:
                # get all the item inside the figure
                if isinstance(subfigure, LTContainer):
                    children_bbox = [extract_item_box(item) for item in subfigure]
                    return determine_max_box(children_bbox)
                break
        except Exception as e:
            logger.error("use default for error since no processor: {}", e)

    return bbox


def extract_pdf_boxs(filename, ignore=0):
    """
    use pdfminer to get the valid area of each page.
    all results are relative position!
    """
    # 打开一个pdf文件
    fp = open(filename, "rb")
    # 创建一个PDF文档解析器对象
    parser = PDFParser(fp)
    # 创建一个PDF文档对象存储文档结构
    # 提供密码初始化，没有就不用传该参数
    # document = PDFDocument(parser, password)
    document = PDFDocument(parser)
    # 检查文件是否允许文本提取
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    # 创建一个PDF资源管理器对象来存储共享资源
    # caching = False不缓存
    rsc_manager = PDFResourceManager(caching=False)
    # 创建一个PDF设备对象
    la_params = LAParams()
    # 创建一个PDF页面聚合对象
    device = PDFPageAggregator(rsc_manager, laparams=la_params)
    # 创建一个PDF解析器对象
    interpreter = PDFPageInterpreter(rsc_manager, device)
    # 处理文档当中的每个页面

    page_boxs = []

    for page in PDFPage.create_pages(document):
        # the page may rotate, clear it to get the corresponding box
        page.rotate = 0

        interpreter.process_page(page)
        # 接受该页面的LTPage对象
        layout = device.get_result()
        # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
        # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
        boxs = extract_box_from_layout(layout, ignore)

        max_box = determine_max_box(boxs)
        page_boxs.append(max_box)

        logger.warning("max visible bbox for the page: {}", max_box)

    return page_boxs


def extract_box_from_layout(layout, ignore):
    boxs = []
    for item in layout:
        box = extract_item_box(item)

        # another process only for `LTRect` with `ignore`
        if isinstance(item, LTRect):
            logger.debug("rect:{}", item)
            # FIXME: some pdf has a global LTRect, case by case
            if ignore > 0:
                ignore -= 1
                continue
        boxs.append(box)
    return boxs
