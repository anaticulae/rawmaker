# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
from functools import partial
from math import sqrt
from typing import List
from typing import Tuple

import utila
from iamraw import BoundingBox
from iamraw import Box
from iamraw import HorizontalLine
from iamraw import PageContentBoxes
from iamraw import PageContentHorizontals
from pdfminer.layout import LTLine
from pdfminer.layout import LTPage
from pdfminer.pdfdocument import PDFDocument
from serializeraw import dump_boxes
from serializeraw import dump_horizontals

from rawmaker.features import process_pagecontent
from rawmaker.features.border import pagesizes
from rawmaker.reader import read

# TODO: LTLine - replace with own data structure to reduce dependencies to
# rawmaker
LineClusters = List[List[LTLine]]

# TODO: HOLY VALUE
VERTICAL_MAX_ERROR = 1.0
# TODO: HOLY VALUE
HORIZONTAL_MIN_WIDTH = 0.6


def work(document: str, pages) -> Tuple[str, str]:
    """Extract content boxes and horizontal lines from given `document`

    Args:
        document(str): path to document
        pages: pages to analyze
    Returns:
        dumped parsed boxes, dumped parsed horizontals
    """
    assert isinstance(document, str), str(document)
    with read(document) as pdf:
        boxes = determine_boxes(pdf, pages=pages)
        horizontal = determine_horizontal(pdf, pages=pages)

    dumped_boxes = dump_boxes(boxes)
    dumped_horizontal = dump_horizontals(horizontal)

    return dumped_boxes, dumped_horizontal


def determine_boxes(document: PDFDocument, pages=None):
    result = determine_clusteritem(
        document,
        determine_pageboxes,
        pages=pages,
    )
    return result


def determine_horizontal(document: PDFDocument, pages=None):
    # prepare worker
    pagewidth = pagesizes(document, pages=pages)[0].size.width
    worker = partial(determine_pagehorizontals, page_width=pagewidth)
    # run worker
    result = determine_clusteritem(
        document,
        worker,
        pages=pages,
    )
    return result


def determine_clusteritem(
        document: PDFDocument,
        collector: callable,
        pages=None,
):
    result = []
    document_lines = lines(document, pages=pages)
    for lines_in_page, page in document_lines:
        lines_in_page = bounding(lines_in_page)
        grouped = determine_cluster(lines_in_page)
        collected = collector(grouped, page)
        result.append(collected)
    return result


def determine_pageboxes(
        cluster: List[LTLine],
        page: int,
) -> PageContentBoxes:
    result = []
    for item in cluster:
        count = len(item)
        if count != 4:
            continue

        x0 = min([min(line[0], line[2]) for line in item])
        y0 = min([min(line[1], line[3]) for line in item])
        x1 = max([max(line[0], line[2]) for line in item])
        y1 = max([max(line[1], line[3]) for line in item])

        box = Box(box=BoundingBox.from_list([x0, y0, x1, y1]))
        result.append(box)
    return PageContentBoxes(content=result, page=page)


def determine_pagehorizontals(
        cluster: LineClusters,
        page: int,
        *,
        page_width: float = 1000,
        vertical_maxerror: float = VERTICAL_MAX_ERROR,
        horizontal_minwidth: float = HORIZONTAL_MIN_WIDTH,
) -> PageContentHorizontals:
    """Collect single line which are expanded horizontal

    Args:
        cluster: list of line cluster
        page(int): current analyzed page

        page_width(float):
        vertical_maxerror(float): maximal vertical difference of the left and
                                  right y-component [0.0,1.0].
        horizontal_minwidth(float): minimum distance between left and right
                                    x-component [0.0,1.0].
    Returns:
        list with horizontal line
    """
    horizontal_minwidth = horizontal_minwidth * page_width
    result = []
    for merged in cluster:
        if len(merged) != 1:
            continue
        x0, y0, x1, y1 = merged[0]
        height = abs(y1 - y0)
        width = abs(x1 - x0)
        assert height >= 0, str(height)
        assert width >= 0, str(width)
        if height < vertical_maxerror and width > horizontal_minwidth:
            horizontal = HorizontalLine(box=BoundingBox.from_list(merged[0]))
            result.append(horizontal)
        else:
            msg = 'no horizontal line %.2f %.2f %.2f %.2f on page: %d'
            utila.debug(msg % (x0, y0, x1, y1, page))
    return PageContentHorizontals(content=result, page=page)


# TODO: Use `utila` cluster code
def determine_cluster(lines: List[BoundingBox]) -> List[BoundingBox]:
    if not lines:
        return []

    # a single element is a cluster
    result = [[item] for item in lines]

    def match(result, current):
        for clusterindex, cluster in enumerate(result):
            for clusteritem in cluster:
                match = [
                    intersecting_lines(clusteritem, test) for test in current
                ]
                if any(match):
                    return clusterindex
        return None

    def cluster(result):
        result, todo = result[0], result[1:]
        if not isinstance(result[0], list):
            result = [result]
        while todo:
            current = todo.pop()
            index = match(result, current)
            if index is None:
                # No match, create new cluster
                result.insert(0, current)
            else:
                result[index].extend(current)
        return result

    # Break when cluster does not change result
    # Cluster till cluster move does not change the result
    before = set()
    while True:
        result = cluster(result)
        hashid = hash(str(result))
        if hashid in before:
            break
        before.add(hashid)
    return result


MIN_DISTANCE = 3


def intersecting_lines(first: BoundingBox, second: BoundingBox):
    """Check if start or end point of two line match

    Args:
        first(BoundingBox):
        second(BoundingBox):
    Returns:
        True if least one elements matches, else False
    """
    # Check only if points intersects
    x0, y0, x2, y2 = first
    x1, y1, x3, y3 = second

    first_distance = min(distance(x0, y0, x1, y1), distance(x0, y0, x3, y3))
    second_distance = min(distance(x2, y2, x3, y3), distance(x2, y2, x1, y1))
    if first_distance < 0.00001 and second_distance < 0.00001:
        # intersecting with themself
        return None

    if first_distance < MIN_DISTANCE:
        return True

    if second_distance < MIN_DISTANCE:
        return True

    return False


def bounding(items):
    """Extract boundingbox out of LT-Element"""
    result = [item.bbox for item in items]
    return result


def pagesize(page: LTPage) -> Tuple[float, float]:
    """Determine `pagesize` from `LTPage`

    Args:
        page(LTPage):
    Returns:
        width and height in 'pixel'
    """
    return (
        page.bbox[2],
        page.bbox[3],
    )


def type_in_document(
        document: PDFDocument,
        datatype,
        pages=None,
) -> List[Tuple[LTPage, int]]:
    """Extract defined `datatype` out of `PDFDocument`

    Hint: the location of pdfminer will be flipped

    Args:
        document(PDFDocument):
        datatype: selected item type
    Returns:
        list with selected item `datatype`
    """
    assert isinstance(document, PDFDocument), type(document)
    result = []
    for page in process_pagecontent(document, pages=pages):
        _, height = pagesize(page.content)
        data = [item for item in page.content if isinstance(item, datatype)]
        # the root of a `PDFDocument` from pdfminer is the left/down-position,
        # a better approach is to define the left/top-position. Therefore the
        # position must flipped.
        for item in data:
            box = item.bbox
            item.bbox = (
                box[0],
                height - box[1],
                box[2],
                height - box[3],
            )
        result.append((data, page.page))
    return result


def lines(document: PDFDocument, pages=None):
    """Extract all `LTLine` out of `PDFDocument` page wise"""
    assert isinstance(document, PDFDocument), type(document)
    return type_in_document(document, LTLine, pages=pages)


def distance(x0, y0, x1, y1):
    return sqrt(pow((x0 - x1), 2) + pow((y1 - y0), 2))


def commandline():
    return utila.Flag(longcut=name(), message='Extract boxes out of document.')


def name():
    return 'boxes'
