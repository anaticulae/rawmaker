# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""The `border`-feature enables to detect the pdf page size in ?pixel?
and locate the cropped box around the content.

Features:
 * page size
 * content size

"""
import collections
import typing

import iamraw
import pdfminer.pdfdocument
import serializeraw
import utila

import rawmaker.features
import rawmaker.reader

PagePageSize = collections.namedtuple('PagePageSize', 'size page')


def work(document: str, pages: tuple = None) -> typing.Tuple[str, str]:
    """Extract page size of `document` bounding boxes of page content.

    Args:
        document: path to document to run parsing
        pages: tuple of processed pages
    Returns:
        tuple(pages, boxes): page size and list of bounding boxes for page
                             content.
    """
    assert isinstance(document, str), str(document)
    with rawmaker.reader.read(document) as pdf:
        sizeandborders, boxes = determine_boundingboxes(pdf, pages=pages)

    pages = serializeraw.dump_pageborders(sizeandborders)
    boundingboxes = serializeraw.dump_boundingboxes(boxes)

    return pages, boundingboxes


def determine_boundingboxes(
        document: pdfminer.pdfdocument.PDFDocument,
        pages: tuple = None,
) -> iamraw.PageBoundingsList:
    """Extract page size, border and boundingboxes from `PDFDocument`.

    Args:
        document(PDFDocument): loaded document
        pages: tuple of processed pages
    Returns:
        sizeandborder(List[PageSizeBorder]) a list for every page with page
                border and a list of the BoundingBoxes of the objects on the
                current page.
        boxes(PageBoundings)
    """
    sizeborders, boxes = [], []
    contentid = 0
    for page, content in rawmaker.features.process_document(document, pages=pages): # yapf:disable
        content, pagenumber = content.content, content.page
        size = pagesize_from_page(page)

        pagebounding = iamraw.PageBoundings(
            boundings=boundingboxes_from_page(content, contentid, size),
            page=pagenumber,
        )
        boxes.append(pagebounding)

        contentid += len(content)
        border = cropborder_from_page(content)
        sizeborders.append(
            iamraw.PageSizeBorder(
                size=size,
                border=border,
                page=pagenumber,
            ))
    return sizeborders, boxes


def pagesizes(
        document: pdfminer.pdfdocument.PDFDocument,
        pages: tuple = None,
) -> typing.List[iamraw.PageSize]:
    """Extract page sizes of `PDFDocument`.

    Args:
        document(PDFDocument): load pdf document
        pages: tuple of processed pages
    Returns:
        List of page sizes.
    """
    result = []
    for page, content in rawmaker.features.process_document(document, pages=pages): # yapf:disable
        content, pagenumber = content.content, content.page
        size = pagesize_from_page(page)
        result.append(PagePageSize(size=size, page=pagenumber))
    return result


def boundingboxes_from_page(
        content: list,
        contentid: int,
        pagesize: tuple,
) -> tuple:
    """Extract bounding boxes from page `content`.

    Args:
        content: content of a single page
        contentid: last id of the previous page
        pagesize: tuple of width and height
    Returns:
        Cropbox which contains all items of this page
    """
    result = []
    for index, item in enumerate(content, start=contentid):
        rounded = tuple([utila.roundme(value) for value in item.bbox])
        # flip y coordinate from top down
        # TODO: REMOVE AFTER UPGRADING PARSER
        # See rawmaker/features/boxes.py
        flipped = [
            rounded[0],
            pagesize.height - rounded[1],
            rounded[2],
            pagesize.height - rounded[3],
        ]
        rounded = tuple([utila.roundme(value) for value in flipped])
        result.append((index, rounded))
    return result


def pagesize_from_page(page: pdfminer.pdfdocument.PDFDocument,
                      ) -> iamraw.PageSize:
    # x, y, width, height
    pagewidth = utila.roundme(page.mediabox[2])
    pageheight = utila.roundme(page.mediabox[3])

    rotate = page.rotate
    if rotate in (90, 270):
        # rotated page, flip page size
        pagewidth, pageheight = pageheight, pagewidth
    return iamraw.PageSize(width=pagewidth, height=pageheight)


def cropborder_from_page(content) -> iamraw.Border:
    if not content:
        return iamraw.Border(None, None, None, None)

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
        utila.roundme(x0),
        utila.roundme(y0),
        utila.roundme(x1),
        utila.roundme(y1),
    )
    assert x0 < x1
    assert y0 < y1

    return iamraw.Border(left=x0, right=x1, top=y0, bottom=y1)


def commandline():
    return utila.Flag(longcut=name(), message='Extract border for every page.')


def name():
    return 'border'
