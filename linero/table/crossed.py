# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
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
    4. Connect small table fragments which are next and close to each other
"""

import operator

import iamraw
import utila

import linero.lines
import linero.table.utils
import linero.table.word
import linero.utils


@utila.profile('strategy:crossed')
def run(lines):
    result = []
    for page in lines:
        extracted = cluster_page(page.content)
        result.append(
            iamraw.PageContentTableBounding(
                page=page.page,
                content=extracted,
            ))
    # remove empty pages
    result = [item for item in result if item.content]
    return result


def cluster_page(lines) -> iamraw.TableBoundings:
    horizontals = linero.table.utils.determine_horizontals(lines)
    verticals = linero.table.utils.determine_verticals(lines)

    result = extract_potential_table(verticals, horizontals)

    result = [
        iamraw.TableBounding(
            bounding=item,
            lines=linero.table.utils.between(
                lines=verticals + horizontals,
                bounding=item,
            ),
        ) for item in result
    ]

    # exclude bounding box, which has two vertical lines
    result = [
        item for item in result
        if len(linero.table.utils.determine_verticals(item.lines)) >= 3
    ]

    result = [
        item for item in result if linero.lines.length_avg(item.lines) >=
        linero.table.TABLE_MIN_AVG_LINE_LENGTH
    ]
    return result


def extract_potential_table(verticals, horizontals):
    if not horizontals:
        utila.debug('skip corossed, no horizontals, extract_potential_table')
        return []
    buckets = utila.Buckets(
        horizontals,
        selector=operator.itemgetter(3),  # y1
    )
    for vertical in verticals:
        x0, top, x1, bottom = vertical
        for item in utila.ranges(top, bottom, 10):
            buckets.add((x0, item, x1, item))

    merged = [index if item else None for index, item in enumerate(buckets)]
    merged = [item for item in utila.groupby_none(merged)]

    tables = []
    for group in merged:
        topline = horizontals[group[0] - 1]
        # double content below table?
        bottomline = horizontals[min((group[-1], len(horizontals) - 1))]

        table = utila.rectangle_max((topline, bottomline))
        tables.append(table)
    tables = linero.table.utils.merge_tables(tables)
    return tables
