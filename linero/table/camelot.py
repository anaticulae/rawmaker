# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

import camelot
import camelot.core
import iamraw
import utila

import rawmaker.features.border


@utila.profile('strategy:camelot')
def run(pdffile: str, pages: tuple = None) -> iamraw.PageContentTableBoundings:
    if pdffile is None:
        # no pdffile given
        utila.error(f'no camelot pdf file given')
        return []
    utila.exists_assert(pdffile)
    # convert internal page definition to camelot definition
    campages = camelot_pages(pages)
    parsed: camelot.core.TableList = camelot.read_pdf(pdffile, pages=campages)
    # group by page number
    result = group_result(parsed, pdffile, pages)
    return result


def group_result(parsed, pdffile, pages) -> iamraw.PageContentTableBoundings:
    # Determine pdf page size to convert to rawmaker bounding definiton.
    sizes = pagesizes(pdffile, pages)
    collected = collections.defaultdict(list)
    for table in parsed:
        pagenumber = zero_based(table.page)
        # Hint: We flip top/down
        bounding = flip_bounding(table._bbox, sizes[pagenumber])  # pylint:disable=W0212
        collected[pagenumber].append(iamraw.TableBounding(bounding=bounding))
    result = [
        iamraw.PageContentTableBounding(page=page, content=content)
        for page, content in collected.items()
    ]
    return result


def flip_bounding(bounding, pagesize) -> iamraw.BoundingBox:
    pageheight = pagesize[1]
    bounding = (
        bounding[0],
        pageheight - bounding[3],
        bounding[2],
        pageheight - bounding[1],
    )
    result = iamraw.BoundingBox.from_list(bounding)
    return result


def zero_based(pagenumber: int) -> int:
    return pagenumber - 1


def camelot_pages(pages: tuple = None) -> str:
    """\
    >>> camelot_pages((1, 2, 3, 4, 5))
    '2,3,4,5,6'
    """
    if not pages:
        return 'all'
    # 1024 is a hack to not determine the max page count
    pages = [
        str(page + 1)
        for page in range(1024)
        if not utila.should_skip(page, pages)
    ]
    result = ','.join(pages)
    return result


def pagesizes(path: str, pages: tuple = None):
    with rawmaker.reader.read(path) as doc:
        sizes = rawmaker.features.border.pagesizes(doc, pages=pages)
    sizes: dict = {size.page: size.size for size in sizes}
    return sizes
