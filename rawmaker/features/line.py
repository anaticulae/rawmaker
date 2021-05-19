# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Line Extractor
==============

This module aims to extract lines out of pdf document. Furthermore the
lines are fixed in x0/x1 and y0/y1, sorted from top to bottom and left
to right and if required merged together.
"""

import operator
import typing

import configo
import iamraw
import pdfminer.pdfdocument
import serializeraw
import utila

import rawmaker.features.boxes
import rawmaker.reader

# maximal difference in y-component
HORIZONTAL_MAX_DIFF = configo.HV_FLOAT_PLUS(default=2.0).value
# maximal difference in x-component
VERTICAL_MAX_DIFF = configo.HV_FLOAT_PLUS(default=2.0).value
# minimal number of minus signs which build a horizontal line
REQUIRED_MINUS_SIGNS = configo.HV_INT_PLUS(default=40).value


def work(document: str, pages: tuple = None) -> str:
    with rawmaker.reader.read(document) as pdf:
        result = determine_lines(pdf, pages=pages)

    dumped = serializeraw.dump_lines(result)
    return dumped


def determine_lines(
    document: pdfminer.pdfdocument.PDFDocument,
    pages: tuple = None,
) -> iamraw.PageContentLines:
    lines_ = lines(document, pages=pages)
    result = []
    for content, number in lines_:
        # left point is left above from right down point
        content = [ensure_position(item) for item in content]
        # top down, left right
        content = sorted(content, key=operator.itemgetter(1, 0))
        # merge lines which are divided by pdf printer
        merged = merge_lines(content)
        result.append(iamraw.PageContentLine(content=merged, page=number))
    return result


def lines(
    pdf: pdfminer.pdfdocument.PDFDocument,
    pages: tuple = None,
) -> list:
    """Extract all `LTLine` out of `PDFDocument` page wise

    Support 3 different types of pdf layout elements:
        LTLine:
        LTRect: small difference between oposite lines
        LTTextBoxHorizontal:

    Args:
        pdf: pdf document to collect lines
        pages: select pages to run anlaysis on
    Returns:
        list of line objects[LTLine, LTRect, LTTextBoxHorizontal]
    """
    assert isinstance(pdf, pdfminer.pdfdocument.PDFDocument), type(pdf)
    possible_lines = type_in_document(
        pdf,
        datatype=(
            pdfminer.layout.LTTextBoxHorizontal,
            pdfminer.layout.LTLine,
            pdfminer.layout.LTRect,
            pdfminer.layout.LTFigure,
            pdfminer.layout.LTCurve,
        ),
        pages=pages,
    )
    strategy = {
        pdfminer.layout.LTLine: accept_ltline,
        pdfminer.layout.LTRect: accept_ltrect,
        pdfminer.layout.LTTextBoxHorizontal: accept_text_as_line,
        pdfminer.layout.LTCurve: accept_curve_as_line,
        pdfminer.layout.LTFigure: accept_figure_as_line,
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
        # convert bounding
        page = [(item.bbox[0], item.bbox[1], item.bbox[2], item.bbox[3])
                for item in page]
        # round bounding
        page = [utila.roundme(item) for item in page]
        # remove very short lines/dots
        page = [item for item in page if not utila.isdot(item, max_length=5.0)]
        # ensure left, top, right, down bounding
        page = [ensure_position(item) for item in page]
        # sort item top down; left right
        page = sorted(page, key=operator.itemgetter(1, 0))
        # merges divided lines
        page = merge_lines(page)
        # remove duplicated lines which mainly produces out of bad figure
        # extraction
        # TODO: ADD LINE DENSITY CHECK?
        page = utila.unique_lines(page, max_diff=3.0)
        result.append((page, pagenumber))
    return result


def accept_text_as_line(item: pdfminer.layout.LTTextBoxHorizontal):
    symbols = ['_', '-', '=']
    for symbol in symbols:
        if item.get_text().count(symbol) >= REQUIRED_MINUS_SIGNS:
            # update bounding to pass vertical error test.
            # use vertical centric position
            # TODO: CHECK THIS: Make it symbol dependend?
            middle = utila.roundme((item.bbox[1] + item.bbox[3]) / 2)
            item.bbox = (item.bbox[0], middle, item.bbox[2], middle)
            return True
    return False


def accept_ltrect(item: pdfminer.layout.LTRect):
    return accept_ltline(item)


def accept_ltline(
    item: pdfminer.layout.LTLine,
    vertical_max_diff=VERTICAL_MAX_DIFF,
    horizontal_max_diff=HORIZONTAL_MAX_DIFF,
) -> bool:
    """Accept horizontal or vertical lines

    The lines must vary only little. A crossing line has vertical
    and horizontal error. We want | or - not / or \\.
    """
    assert item.bbox[3] >= item.bbox[1], str(item.bbox)
    assert item.bbox[0] <= item.bbox[2], str(item.bbox)

    horizontal_error = item.bbox[3] - item.bbox[1] >= horizontal_max_diff
    vertical_error = item.bbox[2] - item.bbox[0] >= vertical_max_diff

    if horizontal_error and vertical_error:
        return False
    return True


def accept_figure_as_line(figure: pdfminer.layout.LTFigure) -> bool:
    """Some pdf renderer converts lines into images."""
    content = figure._objs  # pylint:disable=W0212
    if len(content) != 1:
        return False
    # Do we need a min width? I don't think so because thats the job of
    # later running methods.
    if accept_ltline(content[0]):
        return True
    if figure_special_line(figure):
        return True
    return False


def accept_curve_as_line(curve: pdfminer.layout.LTCurve) -> bool:
    points = curve.pts
    if len(points) == 2:
        # start and end point
        return True
    # more than two points in a row, check if point are on a line
    # [(437.04645, 259.38056), (437.04645, 293.26655), (437.04645, 269.60483999999997)]
    items = [(*first, *second) for first, second in zip(points[:-1], points[1:])] # yapf:disable
    merged = merge_lines(items)
    if len(merged) == 1:
        # all lines in a row
        return True
    return False


def figure_special_line(figure: pdfminer.layout.LTFigure) -> bool:
    """Detect special line and update figure box if figure is special line."""
    # EXAMPLE: MASTER155
    #  'width': 413.96, 'height': 8.54
    # TODO: ANALYZE IMAGE
    image = figure._objs[0]  # pylint:disable=W0212
    height = image.bbox[3] - image.bbox[1]
    width = image.bbox[2] - image.bbox[0]
    ratio = width / height
    if width <= 350:  # TODO: HOLY VALUE
        return False
    if ratio <= 45.0:  # TODO: HOLY VALUE
        return False
    # adjust bounding of figure to middle line
    # TODO: USE IMAGE INFORMATION
    middle = utila.roundme((figure.bbox[1] + figure.bbox[3]) / 2)
    figure.bbox = (figure.bbox[0], middle, figure.bbox[2], middle)
    return True


def merge_lines(items, diff: float = 3.0):  # TODO: HOLY VALUE
    """Some pdf printer prints long lines as a couple of short lines.
    For analysis it is required, that these lines are merged to single
    lines to work with correct length and positon.

    This algorithm merges lines which are:
     - connected in two points
     - have the same raising.

    As a requirement, the lines are sorted top down and left right.

    >>> merge_lines([(328.18, 373.08, 329.68, 373.83),
    ...              (329.68, 373.08, 416.03, 373.83),
    ...              (416.02, 373.08, 416.77, 373.83),
    ...              (416.77, 373.08, 502.39, 373.83),
    ...              (502.40, 373.08, 504.65, 373.83),])
    [(328.18, 373.08, 504.65, 373.83)]

    >>> merge_lines([(257.58, 440.65 ,259.08 ,442.15),
    ...              (259.08, 440.65 ,328.18 ,442.15),
    ...              (328.18, 440.65 ,329.68 ,442.15),
    ...              (329.68, 440.65 ,416.03 ,441.40),
    ...              (416.02, 440.65 ,416.77 ,442.15),
    ...              (416.77, 440.65 ,502.39 ,441.40),
    ...              (502.40, 440.65 ,504.65 ,442.15)])
    [(257.58, 440.65, 504.65, 442.15)]
    """
    if not items:
        return []
    result = [items[0]]
    for item in items[1:]:
        last_x1, last_y1 = result[-1][2], result[-1][3]
        x0, y0 = item[0], item[1]
        if not all((
                utila.near(last_x1, x0, diff=diff),
                utila.near(last_y1, y0, diff=diff),
                utila.near(
                    raising(item, diff),
                    raising(result[-1], diff),
                    diff=diff,
                ),
        )):
            result.append(item)
        else:
            # unite
            new = (result[-1][0], result[-1][1], item[2], item[3])
            result.pop()
            result.append(new)

    # sort item top down; left right after merging
    result = sorted(result, key=operator.itemgetter(1, 0))
    return result


def raising(item, diff=1.0) -> float:
    """\
    >>> raising((0, 0, 50, 50))
    1.0
    >>> raising((0, 0, 0, 100)) # inf raising
    2147483647
    """
    xdiff = (item[2] - item[0])
    ydiff = (item[3] - item[1])
    if -diff <= ydiff <= diff:
        return 0.0
    if -diff <= xdiff <= diff:
        return utila.INF
    return xdiff / ydiff


def ensure_position(item: tuple) -> tuple:
    x0, y0, x1, y1 = item
    x0, x1 = min([x0, x1]), max([x0, x1])
    y0, y1 = min([y0, y1]), max([y0, y1])
    return (x0, y0, x1, y1)


def type_in_document(
    document: pdfminer.pdfdocument.PDFDocument,
    datatype: object,
    pages: tuple = None,
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
