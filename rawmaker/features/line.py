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

This module aims to extract lines out of pdf document.
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
        # convert LTLine to tuple of boundingbox(x0,y0,x1,y1)
        content = [bbox_tobounding(item.bbox) for item in content]
        # left point is left above from right down point
        content = [ensure_position(item) for item in content]
        # top down, left right
        content = sorted(content, key=operator.itemgetter(0, 1))
        result.append(iamraw.PageContentLine(content=content, page=number))
    return result


def ensure_position(item: tuple) -> tuple:
    x0, y0, x1, y1 = item
    x0, x1 = min([x0, x1]), max([x0, x1])
    y0, y1 = min([y0, y1]), max([y0, y1])
    return (x0, y0, x1, y1)


def bbox_tobounding(bbox) -> tuple:
    return tuple([utila.roundme(var) for var in bbox])
