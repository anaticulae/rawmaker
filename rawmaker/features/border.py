# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from collections import namedtuple
from typing import List
from typing import Tuple

from iamraw import Border
from iamraw import PageBoundings
from iamraw import PageBoundingsList
from iamraw import PageSize
from iamraw import PageSizeBorder
from pdfminer.pdfdocument import PDFDocument
from serializeraw import dump_boundingboxes
from serializeraw import dump_pageborders
from utila import Flag
from utila import roundme

from rawmaker.features import process_document
from rawmaker.reader import read

PagePageSize = namedtuple('PagePageSize', 'size page')


def work(document: str) -> Tuple[str, str]:
    """Extract page-size of `document` bounding boxes of page-content

    Args:
        document: pdf-document to run parsing
    Returns:
        tuple(pages, boxes): page size and list of bounding boxes for page
        content
    """
    assert isinstance(document, str), str(document)
    with read(document) as pdf:
        sizeandborders, boxes = determine_boundingboxes(pdf)

    pages = dump_pageborders(sizeandborders)
    boundingboxes = dump_boundingboxes(boxes)

    return pages, boundingboxes


def determine_boundingboxes(document: PDFDocument) -> PageBoundingsList:
    """Extract page size, border and boundingboxes from `PDFDocument`

    Args:
        document(PDFDocument):
    Returns:
        sizeandborder(List[PageSizeBorder]) a list for every page with page
                border and a list of the BoundingBoxes of the objects on the
                current page.
        boxes(PageBoundings)
    """
    sizeborders, boxes = [], []
    contentid = 0
    for page, content in process_document(document):
        content, pagenumber = content.content, content.page
        size = pagesize_from_page(page)

        pagebounding = PageBoundings(
            boundings=boundingboxes_from_page(content, contentid),
            page=pagenumber,
        )
        boxes.append(pagebounding)

        contentid += len(content)
        border = cropborder_from_page(content)
        sizeborders.append(
            PageSizeBorder(
                size=size,
                border=border,
                page=pagenumber,
            ))
    return sizeborders, boxes


def pagesizes(document: PDFDocument, pages=None) -> List[PageSize]:
    """Extract page sizes of `PDFDocument`

    Args:
        document(PDFDocument):
        pages:
    Returns:
    """
    result = []
    for page, content in process_document(document):
        content, pagenumber = content.content, content.page
        size = pagesize_from_page(page)
        result.append(PagePageSize(size=size, page=pagenumber))
    return result


def boundingboxes_from_page(content, contentid: int):
    """Extract bounding boxes from page `content`

    Args:
        content: content of a single page
        contentid: last id of the previous page
    """
    result = []
    for index, item in enumerate(content, start=contentid):
        rounded = [roundme(value) for value in item.bbox]
        result.append([index, rounded])
    return result


def pagesize_from_page(page) -> PageSize:
    # x, y, width, height
    pagewidth = roundme(page.mediabox[2])
    pageheight = roundme(page.mediabox[3])

    return PageSize(width=pagewidth, height=pageheight)


def cropborder_from_page(content) -> Border:
    if not content:
        return Border(None, None, None, None)

    # Convert pdfminer coordinate to own system, see `BoundingBox`
    # TODO: Create convertion method in `BoundingBox`
    # left, bottom, right, top
    height = content.bbox[3]
    x0 = min([item.bbox[0] for item in content])
    y0 = min([height - item.bbox[3] for item in content])
    x1 = max([item.bbox[2] for item in content])
    y1 = max([height - item.bbox[1] for item in content])
    # left, right, top, bottom
    x0, y0, x1, y1 = (
        roundme(x0),
        roundme(y0),
        roundme(x1),
        roundme(y1),
    )
    assert x0 < x1
    assert y0 < y1

    return Border(left=x0, right=x1, top=y0, bottom=y1)


def commandline():
    return Flag(longcut=name(), message='Extract border for every page.')


def name():
    return 'border'
