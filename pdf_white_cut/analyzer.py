#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from numpy import isin

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import *
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser

from pdf_white_cut.logger import logger


def get_max_box(box_list):
    res = [
        sys.maxsize,
        sys.maxsize,
        -sys.maxsize,
        -sys.maxsize,
    ]
    for box in box_list:
        if box is None:
            continue
        for idx, (a, b) in enumerate(zip(res, box)):
            if idx < 2:
                res[idx] = min(a, b)
            else:
                res[idx] = max(a, b)

    return tuple(res)


def extract_box(item):
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
        logger.warning("NotImplemented and use itself: {}", item)
    elif isinstance(item, LTTextLine):
        # there is 2 types of `LTTextLine`: horizontal and vertical
        text = item.get_text().encode("unicode_escape")
        logger.debug("analyse LTTextLine: {} {}", item, text)
        # TODO: here we ignored fonts and text line direction, may error in some cases
        # since the text has a height on y-axis, or has a width on x-axis,
        # we must modify it to make the whole text visible
        # FIXME: no we use `half` for upper and lower, may not right but work
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
        logger.warning("NotImplemented and use itself: {}", item)
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
                    children_bbox = [extract_box(item) for item in subfigure]
                    return get_max_box(children_bbox)
                break
        except Exception as e:
            logger.error("use default for error since no processor: {}", e)

    return bbox


def analyse_pdf(filename, ignore=0):
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

    visible_boxs = []

    # doc.get_pages() 获取page列表
    # for i, page in enumerate(document.get_pages()):
    # PDFPage.create_pages(document) 获取page列表的另一种方式
    # 循环遍历列表，每次处理一个page的内容
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        # 接受该页面的LTPage对象
        layout = device.get_result()
        # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
        # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
        box_list = []
        for item in layout:
            box = extract_box(item)

            # another process only for `LTRect` with `ignore`
            if isinstance(item, LTRect):
                logger.debug("rect:{}", item)
                # FIXME: some pdf has a global LTRect, case by case
                if ignore > 0:
                    ignore -= 1
                    continue
            box_list.append(box)

        visible_box = get_max_box(box_list)
        logger.warning("visible bbox: {}", visible_box)
        visible_boxs.append(visible_box)

    logger.warning("visible bbox for the page: {}", visible_boxs)
    return visible_boxs
