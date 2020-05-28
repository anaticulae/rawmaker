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

import iamraw
import pdfminer.pdfdocument
import serializeraw
import utila

import rawmaker.features.boxes
import rawmaker.reader


def work(document: str, pages: tuple = None) -> str:
    with rawmaker.reader.read(document) as pdf:
        lines = determine_lines(pdf, pages=pages)

    dumped = serializeraw.dump_lines(lines)
    return dumped


def determine_lines(
        document: pdfminer.pdfdocument.PDFDocument,
        pages: tuple = None,
) -> iamraw.PageContentLines:
    lines = rawmaker.features.boxes.lines(document, pages=pages)
    result = []
    for content, number in lines:
        # left point is left above from right down point
        content = [ensure_position(item) for item in content]
        # top down, left right
        content = sorted(content, key=operator.itemgetter(1, 0))
        # merge lines which are divided by pdf printer
        merged = merge_lines(content)
        result.append(iamraw.PageContentLine(content=merged, page=number))
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


def bbox_tobounding(bbox) -> tuple:
    return tuple([utila.roundme(var) for var in bbox])
