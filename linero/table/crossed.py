# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Table Extraction Strategy: Crossed:
===================================

Detect tables which are build out of horizontal lines which are
connected due vertical lines.

Strategy:
    1. Add buckets with horizontal lines
    2. Iter thru vertical lines and add boundings in every hitted bucket
    3. Select connected buckets
    4. Connect small table framents which are next and close to each other
"""

import operator

import iamraw
import utila

import linero.lines
import linero.utils


def run(lines):
    result = []
    for page in lines:
        extracted = cluster_page(page.content)
        result.append(
            iamraw.PageContentTableBounding(
                page=page.page,
                content=extracted,
            ))
    return result


def cluster_page(lines) -> iamraw.TableBoundings:
    horizontals = [
        item for item in lines
        if linero.lines.horizontal(item, maxdiff=4.0)  # TODO: HOLY VALUE
    ]
    verticals = [
        item for item in lines
        if linero.lines.vertical(item, maxdiff=4.0)  # TODO: HOLY VALUE
    ]
    if len(verticals) <= 3:
        # TODO: TOO FEW VERTICALS FOR THIS ALGO
        return []

    result = extract_potential_table(verticals, horizontals)

    # TODO: ADD LINES
    result = [iamraw.TableBounding(bounding=item) for item in result]
    return result


def extract_potential_table(verticals, horizontals):
    buckets = utila.Buckets(
        horizontals,
        selector=operator.itemgetter(3),  # y1
    )
    for vertical in verticals:
        top, y0, bottom, y1 = vertical
        for item in ranges(top, bottom, 10):
            buckets.add((item, y0, item, y1))

    merged = [index if item else None for index, item in enumerate(buckets)]
    merged = [item for item in utila.groupby_none(merged)]

    tables = []
    for group in merged:
        topline = horizontals[group[0] - 1]
        # double content below table?
        bottomline = horizontals[min((group[-1], len(horizontals) - 1))]
        table = linero.table.utils.table_bounding((topline, bottomline))
        tables.append(table)
    tables = linero.table.utils.merge_tables(tables)
    return tables


def ranges(start, stop, step):
    assert start <= stop
    assert step > 0

    while start < stop:
        yield start
        start += step
