# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
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
                # TODO: CHECK THIS: Make it symbol dependend?
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
        # convert bounding
        page = [(item.bbox[0], item.bbox[1], item.bbox[2], item.bbox[3])
                for item in page]
        # round bounding
        page = [utila.roundme(item) for item in page]
        # ensure left, top, right, down bounding
        page = [ensure_position(item) for item in page]
        # sort item top down; left right
        page = sorted(page, key=operator.itemgetter(1, 0))
        # merges divided lines
        page = merge_lines(page)

        result.append((page, pagenumber))
    return result


def merge_lines(items):
    """Some pdf printer prints long lines as a couple of short lines.
    For analysis it is required, that these lines are merged to single
    lines to work with correct length and positon.

    This algorithm merges lines which are:
     - connected in two points
     - have the same raising.

    As a requirement, the lines are sorted top down and left right.
    """
    if not items:
        return []
    result = [items[0]]
    for item in items[1:]:
        last_x1, last_y1 = result[-1][2], result[-1][3]
        x0, y0 = item[0], item[1]
        if not all((
                utila.near(last_x1, x0, diff=0.001),
                utila.near(last_y1, y0, diff=0.001),
                utila.near(raising(item), raising(result[-1]), diff=0.001),
        )):
            result.append(item)
        else:
            # unite
            new = (result[-1][0], result[-1][1], item[2], item[3])
            result.pop()
            result.append(new)
    return result


# TODO: MOVE TO UTILA
def zero(item):
    return utila.near(item, 0.0, 0.0001)


utila.zero = zero


def raising(item) -> float:
    xdiff = (item[2] - item[0])
    ydiff = (item[3] - item[1])
    if utila.zero(ydiff):
        return 0.0
    if utila.zero(xdiff):
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
