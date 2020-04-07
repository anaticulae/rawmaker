# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import functools
import math
import operator
import typing

import configo
import iamraw
import pdfminer.layout
import serializeraw
import utila

import rawmaker.features
import rawmaker.features.border
import rawmaker.features.line
import rawmaker.reader

# TODO: LTLine - replace with own data structure to reduce dependencies to
# rawmaker
LineClusters = typing.List[typing.List[pdfminer.layout.LTLine]]

# minimal length of a horizontal line
HORIZONTAL_MIN_WIDTH = configo.HV_FLOAT(default=0.2).value
# maximal difference in y-component
HORIZONTAL_MAX_DIFF = configo.HV_FLOAT_PLUS(default=2.0).value
# maximal difference in x-component
VERTICAL_MAX_DIFF = configo.HV_FLOAT_PLUS(default=2.0).value
# minimal number of minus signs which build a horizontal line
REQUIRED_MINUS_SIGNS = configo.HV_INT_PLUS(default=40).value


def work(document: str, pages: tuple) -> typing.Tuple[str, str]:
    """Extract content boxes and horizontal lines from given `document`

    Args:
        document(str): path to document
        pages(tuple): pages to analyze
    Returns:
        dumped parsed boxes, dumped parsed horizontals
    """
    assert isinstance(document, str), str(document)
    with rawmaker.reader.read(document) as pdf:
        boxes = determine_boxes(pdf, pages=pages)
        horizontal = determine_horizontal(pdf, pages=pages)

    dumped_boxes = serializeraw.dump_boxes(boxes)
    dumped_horizontal = serializeraw.dump_horizontals(horizontal)

    return dumped_boxes, dumped_horizontal


def determine_boxes(
        document: pdfminer.pdfdocument.PDFDocument,
        pages=None,
):
    result = determine_clusteritem(
        document,
        determine_pageboxes,
        pages=pages,
    )
    return result


def determine_horizontal(
        document: pdfminer.pdfdocument.PDFDocument,
        pages=None,
):
    # prepare worker
    pagewidth = rawmaker.features.border.pagesizes(document, pages=pages)
    pagewidth = pagewidth[0].size.width
    worker = functools.partial(determine_pagehorizontals, page_width=pagewidth)
    # run worker
    result = determine_clusteritem(
        document,
        worker,
        pages=pages,
    )
    return result


def determine_clusteritem(
        document: pdfminer.pdfdocument.PDFDocument,
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
        cluster: typing.List[pdfminer.layout.LTLine],
        page: int,
) -> iamraw.PageContentBoxes:
    result = []
    for item in cluster:
        count = len(item)
        if count != 4:
            continue

        x0 = min([min(line[0], line[2]) for line in item])
        y0 = min([min(line[1], line[3]) for line in item])
        x1 = max([max(line[0], line[2]) for line in item])
        y1 = max([max(line[1], line[3]) for line in item])

        box = iamraw.Box(box=iamraw.BoundingBox.from_list([x0, y0, x1, y1]))
        result.append(box)
        # ensure to sort items top to bottom and left to right
        result = sorted(result, key=operator.attrgetter('box.y0', 'box.x0'))
    return iamraw.PageContentBoxes(content=result, page=page)


def determine_pagehorizontals(
        cluster: LineClusters,
        page: int,
        *,
        page_width: float = 1000,
        vertical_maxerror: float = VERTICAL_MAX_DIFF,
        horizontal_minwidth: float = HORIZONTAL_MIN_WIDTH,
) -> iamraw.PageContentHorizontals:
    """Collect single line which are expanded horizontal

    Args:
        cluster: list of line cluster
        page(int): current analyzed page

        page_width(float): width of page page
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
        # convert from BoundingBox
        x0, y0, x1, y1 = utila.roundme(tuple(merged[0]))
        height = abs(y1 - y0)
        width = abs(x1 - x0)
        assert height >= 0, str(height)
        assert width >= 0, str(width)
        if height < vertical_maxerror and width > horizontal_minwidth:
            box = iamraw.BoundingBox.from_list(merged[0])
            horizontal = iamraw.HorizontalLine(box=box)
            result.append(horizontal)
        else:
            utila.debug(f'no horizontal line {x0} {y0} {x1} {y1}; page: {page}')
    # ensure to sort items top to bottom and left to right
    result = sorted(result, key=operator.attrgetter('box.y0', 'box.x0'))
    return iamraw.PageContentHorizontals(content=result, page=page)


def determine_cluster(items: iamraw.BoundingBoxes) -> iamraw.BoundingBoxes:  # pylint:disable=R1260
    if not items:
        return []

    # a single element is a cluster
    result = [[item] for item in items]

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


def intersecting_lines(
        first: iamraw.BoundingBox,
        second: iamraw.BoundingBox,
) -> bool:
    """Check if start or end point of two line match.

    Args:
        first(BoundingBox): line to cross
        second(BoundingBox): line to cross
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


def pagesize(page: pdfminer.layout.LTPage) -> typing.Tuple[float, float]:
    """Determine `pagesize` from `LTPage`.

    Args:
        page(LTPage): page to determine page size
    Returns:
        tuple of width and height in 'pixel'
    """
    return (page.bbox[2], page.bbox[3])


def type_in_document(
        document: pdfminer.pdfdocument.PDFDocument,
        datatype: object,
        pages=None,
) -> typing.List[typing.Tuple[pdfminer.layout.LTPage, int]]:
    """Extract defined `datatype` out of `PDFDocument`

    Args:
        document(PDFDocument): pdf document to extract all types
        datatype: selected item type
        pages(tuple): select pages
    Returns:
        List with selected `datatype`.
    """
    assert isinstance(document, pdfminer.pdfdocument.PDFDocument), type(document) # yapf:disable
    result = []
    for page in rawmaker.features.process_pagecontent(document, pages=pages):
        data = [item for item in page.content if isinstance(item, datatype)]
        result.append((data, page.page))
    return result


def lines(  # pylint:disable=R1260
        document: pdfminer.pdfdocument.PDFDocument,
        pages: tuple = None,
) -> list:
    """Extract all `LTLine` out of `PDFDocument` page wise

    Support 3 different types of pdf layout elements:
        LTLine:
        LTRect: small difference between oposite lines
        LTTextBoxHorizontal:

    Args:
        document: pdf document to collect lines
        pages: select pages to run anlaysis on
    Returns:
        list of line objects[LTLine, LTRect, LTTextBoxHorizontal]
    """
    assert isinstance(document, pdfminer.pdfdocument.PDFDocument), type(document) # yapf:disable
    possible_lines = type_in_document(
        document,
        datatype=(
            pdfminer.layout.LTLine,
            pdfminer.layout.LTRect,
            pdfminer.layout.LTTextBoxHorizontal,
        ),
        pages=pages,
    )

    def accept_text_as_line(item: pdfminer.layout.LTTextBoxHorizontal):
        symbols = ['_', '-', '=']
        for symbol in symbols:
            if item.get_text().count(symbol) >= REQUIRED_MINUS_SIGNS:
                # update bounding to pass vertical error test.
                # use vertical centric position
                middle = utila.roundme((item.bbox[1] + item.bbox[3]) / 2)
                item.bbox = (item.bbox[0], middle, item.bbox[2], middle)
                return True
        return False

    def accept_ltrect(item: pdfminer.layout.LTRect):
        return accept_ltline(item)

    def accept_ltline(item: pdfminer.layout.LTLine):
        """Accept horizontal or vertical lines

        The lines must vary only little. A crossing line has vertical
        and horizontal error. We want | or - not / or \\.
        """
        assert item.bbox[3] >= item.bbox[1], str(item.bbox)
        assert item.bbox[0] <= item.bbox[2], str(item.bbox)

        horizontal_error = item.bbox[3] - item.bbox[1] >= HORIZONTAL_MAX_DIFF
        vertical_error = item.bbox[2] - item.bbox[0] >= VERTICAL_MAX_DIFF

        if horizontal_error and vertical_error:
            return False
        return True

    strategy = {
        pdfminer.layout.LTLine: accept_ltline,
        pdfminer.layout.LTRect: accept_ltrect,
        pdfminer.layout.LTTextBoxHorizontal: accept_text_as_line,
    }
    result = []
    for content, pagenumber in possible_lines:
        page = []
        for item in content:
            # check item against strategy. If no stategy is supported, the
            # element is skipped.
            try:
                if not strategy[type(item)](item):
                    continue
                page.append(item)
            except KeyError:
                utila.error(f'unsupported strategy {item}')
        result.append((
            page,
            pagenumber,
        ))
    return result


def distance(x0, y0, x1, y1):
    return math.sqrt(pow(x1 - x0, 2) + pow(y1 - y0, 2))


def commandline():
    return utila.Flag(longcut=name(), message='Extract boxes out of document.')


def name():
    return 'boxes'
