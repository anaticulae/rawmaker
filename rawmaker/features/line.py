# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Line Extractor
===============

This module aims to extract lines out of pdf document.
"""

import collections
import operator
import typing

import pdfminer.pdfdocument
import utila
import yaml

import rawmaker.features.boxes
import rawmaker.reader

# TODO MOVE to iamraw
PageContentLine = collections.namedtuple('PageContentLine', 'page, content')
PageContentLines = typing.List[PageContentLine]


def work(document: str, pages: tuple = None) -> str:
    with rawmaker.reader.read(document) as pdf:
        lines = determine_lines(pdf, pages=pages)

    dumped = dump_lines(lines)
    return dumped


def determine_lines(
        document: pdfminer.pdfdocument.PDFDocument,
        pages: tuple = None,
) -> PageContentLines:
    lines = rawmaker.features.boxes.lines(document, pages=pages)
    result = []
    for content, number in lines:
        # convert LTLine to tuple of boundingbox(x0,y0,x1,y1)
        content = [bbox_tobounding(item.bbox) for item in content]
        # left point is left above from right down point
        content = [ensure_position(item) for item in content]
        # top down, left right
        content = sorted(content, key=operator.itemgetter(0, 1))
        result.append(PageContentLine(content=content, page=number))
    return result


def ensure_position(item: tuple) -> tuple:
    x0, y0, x1, y1 = item
    x0, x1 = min([x0, x1]), max([x0, x1])
    y0, y1 = min([y0, y1]), max([y0, y1])
    return (x0, y0, x1, y1)


def bbox_tobounding(bbox) -> tuple:
    return tuple([utila.roundme(var) for var in bbox])


def dump_lines(lines: PageContentLines) -> str:
    lines = sorted(lines, key=lambda x: x.page)
    result = []
    for page in lines:
        content = ['%.2f %.2f %.2f %.2f' % item for item in page.content]
        raw = {'page': page.page, 'content': content}
        result.append(raw)
    dumped = yaml.dump(result)
    return dumped


def load_lines(content: str, pages: tuple = None) -> PageContentLines:
    content = utila.from_raw_or_path(content, ftype='yaml')
    loaded = yaml.load(content, Loader=yaml.FullLoader)
    result = []
    for page in loaded:
        pagenumber = int(page['page'])
        if utila.should_skip(pagenumber, pages):
            continue
        content = []
        for raw in page['content']:
            item = tuple(utila.roundme(float(var)) for var in raw.split())
            content.append(item)
        result.append(PageContentLine(page=pagenumber, content=content))
    return result
