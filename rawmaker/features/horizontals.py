# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Horizontals
===========

Whats the difference between `boxes_horizontals` and `lines`?
`boxes_horizontals` contain only vertical lines. `lines` can contain
every lines in every direction.

Why do we cluster for horizontal lines?
To ignore lines which are part of a box and can not be a horizontal line.
"""

import functools
import operator
import typing

import configo
import iamraw
import pdfminer.layout
import serializeraw
import utila

import rawmaker.features
import rawmaker.features.border
import rawmaker.features.boxes
import rawmaker.reader

# TODO: LTLine - replace with own data structure to reduce dependencies to
# rawmaker
LineClusters = typing.List[typing.List[pdfminer.layout.LTLine]]

# minimal length of a horizontal line
HORIZONTAL_MIN_WIDTH = configo.HV_FLOAT(default=0.2).value
# maximal difference in x-component
HORIZONTAL_VERTICAL_MAX_DIFF = configo.HV_FLOAT_PLUS(default=2.0).value


def work(lines: str, pages: tuple) -> str:
    """Extract content horizontal lines from given `document`

    Args:
        lines(str): path to document
        pages(tuple): pages to analyze
    Returns:
        dumped parsed boxes, dumped parsed horizontals
    """
    assert isinstance(lines, str), type(lines)
    lines = serializeraw.load_lines(lines, pages=pages)
    horizontal = determine_horizontal(lines)
    dumped = serializeraw.dump_horizontals(horizontal)
    return dumped


def determine_horizontal(lines, pagewidth=500):
    worker = functools.partial(determine_pagehorizontals, page_width=pagewidth)
    # run worker
    result = rawmaker.features.boxes.determine_clusteritem(
        lines,
        worker,
    )
    return result


def determine_pagehorizontals(
        cluster: LineClusters,
        page: int,
        *,
        page_width: float,
        vertical_maxerror: float = HORIZONTAL_VERTICAL_MAX_DIFF,
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
            # ignore boxed lines
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
