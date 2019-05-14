# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from iamraw import Border
from iamraw import PageSize
from pdfminer.pdfdocument import PDFDocument
from serializeraw import dump_boundingboxes
from serializeraw import dump_pageborders
from serializeraw.border import NDIGITS
from utila import Flag

from rawmaker.features import process_document


def work(document: PDFDocument):
    """Extract bounding boxes of page content and page size of `document`

    Args:
        document: pdf-document to run parsing
    Returns:
        tuple(pages, boxes): page size and list of bounding boxes for page
        content
    """
    size, border, boxes = determine_bounding_box(document)
    return {
        'pages': dump_pageborders(size, border),
        'boxes': dump_boundingboxes(boxes),
    }


def determine_bounding_box(document: PDFDocument):
    """Extract pagesizes and boundingboxes from `PDFDocument`"""
    pagesize, border, boxes = [], [], []
    contentid = 0
    for page, content in process_document(document):
        pagesize.append(pagesize_from_page(page))
        boxes.append(boxes_from_page(content, contentid))
        contentid += len(content)
        border.append(cropborder_from_page(content))
    return pagesize, border, boxes


def boxes_from_page(content, contentid: int):
    """Extract bounding boxes from page `content`

    Args:
        content: content of a single page
        contentid: last id of the previous page
    """
    result = []
    for index, item in enumerate(content, start=contentid):
        rounded = [round(value, NDIGITS) for value in item.bbox]
        result.append([index, rounded])
    return result


def pagesize_from_page(page) -> PageSize:
    # x, y, width, height
    pagewidth = round(page.mediabox[2], NDIGITS)
    pageheight = round(page.mediabox[3], NDIGITS)

    return PageSize(width=pagewidth, height=pageheight)


def cropborder_from_page(content) -> Border:
    if not content:
        return Border(None, None, None, None)

    x0 = min([item.bbox[0] for item in content])
    y0 = min([item.bbox[1] for item in content])
    x1 = max([item.bbox[2] for item in content])
    y1 = max([item.bbox[3] for item in content])

    x0, y0, x1, y1 = (
        round(x0, NDIGITS),
        round(y0, NDIGITS),
        round(x1, NDIGITS),
        round(y1, NDIGITS),
    )
    assert x0 < x1
    assert y0 < y1

    return Border(left=x0, right=x1, top=y1, bottom=y0)


def commandline():
    return Flag(longcut=name(), message='Extract border for every page')


def name():
    return 'border'
