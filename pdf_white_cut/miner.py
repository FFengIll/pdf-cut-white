#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

try:
    from pdfminer.converter import PDFPageAggregator
    from pdfminer.pdfparser import PDFParser
    from pdfminer.pdfdocument import PDFDocument
    from pdfminer.pdfpage import PDFPage
    from pdfminer.pdfpage import PDFTextExtractionNotAllowed
    from pdfminer.pdfinterp import PDFResourceManager
    from pdfminer.pdfinterp import PDFPageInterpreter
    from pdfminer.layout import *
except:
    pass
try:
    from pdfminer3.converter import PDFPageAggregator
    from pdfminer3.pdfparser import PDFParser
    from pdfminer3.pdfdocument import PDFDocument
    from pdfminer3.pdfpage import PDFPage
    from pdfminer3.pdfpage import PDFTextExtractionNotAllowed
    from pdfminer3.pdfinterp import PDFResourceManager
    from pdfminer3.pdfinterp import PDFPageInterpreter
    from pdfminer3.layout import *
except:
    pass

import loguru

logger = loguru.logger


def get_max_box(box_list):
    res = [
        sys.maxsize,
        sys.maxsize,
        -sys.maxsize,
        -sys.maxsize,
    ]
    for box in box_list:
        for idx, (a, b) in enumerate(zip(res, box)):
            if idx < 2:
                res[idx] = min(a, b)
            else:
                res[idx] = max(a, b)

    return tuple(res)


def mine_area(filename, ignore=0):
    """
    use pdfminer to get the valid area of each page.
    all results are relative position!
    """
    # 打开一个pdf文件
    fp = open(filename, 'rb')
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

    page_visible = []

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
            box = item.bbox

            if isinstance(item, LTTextBoxHorizontal):
                pass
            elif isinstance(item, LTTextBox) or isinstance(item, LTTextLine):
                # text
                logger.debug('text{}', item)
                logger.debug(item.get_text())
                # the text has a height on y axis, so we must modify it
                box = box[0], box[1] - item.height, box[2], box[3]
            elif isinstance(item, LTImage):
                logger.debug('image:{}', item)
            elif isinstance(item, LTFigure):
                logger.debug('figure:{}', item)
            elif isinstance(item, LTAnno):
                logger.debug('anno:{}', item)
            elif isinstance(item, LTChar):
                logger.debug('char:{}', item)
            elif isinstance(item, LTLine):
                logger.debug('line:{}', item)
            elif isinstance(item, LTRect):
                logger.debug('rect:{}', item)
                # FIXME: some pdf has a global LTRect, case by case
                if ignore > 0:
                    ignore -= 1
                    continue
            elif isinstance(item, LTCurve):
                logger.debug('curve:{}', item)

            box_list.append(box)

        visible_box = get_max_box(box_list)
        logger.warning(visible_box)
        page_visible.append(visible_box)

    logger.warning(page_visible)
    return page_visible
