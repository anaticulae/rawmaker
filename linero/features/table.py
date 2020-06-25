# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Table Extractro
===============

TODO: MOVE TO LINTER

Some tables contains double lines which indicates that is something wrong.

Example:

    If you add in word a table line and do not add any content add minize the
    height of the line with your cursor.
    Indicates that table are styled different.

"""

import math
import operator

import configo
import iamraw
import serializeraw
import utila

import linero.cluster
import linero.lines
import linero.table
import linero.utils


def work(
        text: str,
        textposition: str,
        lines: str,
        pages: tuple = None,
) -> str:
    lines = serializeraw.load_lines(lines, pages=pages)

    navigators = serializeraw.create_pagetextnavigators_fromfile(
        text,
        textposition,
        pages=pages,
    )

    result = []
    for navigator in navigators:
        pagelines = utila.select_page(lines, page=navigator.page)
        if pagelines:
            extracted = cluster_page(navigator, pagelines.content)
        else:
            extracted = []
        result.append(
            iamraw.PageContentTableBounding(
                page=navigator.page,
                content=extracted,
            ))
    dumped = serializeraw.dump_tables(result)
    return dumped


def cluster_page(navigator, lines) -> iamraw.TableBoundings:
    horizontals = [
        item for item in lines
        if linero.lines.horizontal(item, maxdiff=4.0)  # TODO: HOLY VALUE
    ]

    if len(horizontals) <= 2:
        # TODO: SINGLE LINE TABLE?
        return []

    boundings = [item.bounding for item in navigator]
    boundings = linero.utils.sort_leftright_topdown(boundings)

    result = []
    grouped_horizontals = linero.table.group_horizontals(horizontals)
    for group in grouped_horizontals:
        # if len(group) <= 2:
        #     continue
        double_table = extract_potential_table(
            boundings,
            group,
            min_elements=2,
        )

        single_table = extract_potential_table(
            boundings,
            group,
            min_elements=1,
        )

        tables = double_table
        if len(single_table) > len(double_table):
            tables = single_table

        tables = [
            # judge tables
            item
            for item in tables
            if linero.table.valid_table(item, navigator)
        ]

        # merge connected tables
        tables = linero.table.merge_tables(tables)

        result.extend(tables)

    # TODO: ADD LINES
    result = [iamraw.TableBounding(bounding=item) for item in result]
    return result


def extract_potential_table(boundings, horizontals, min_elements=2):
    clustered = linero.utils.same_line_cluster(
        boundings,
        min_elements=min_elements,
    )

    if not clustered:
        return []

    singles = [item for item in clustered if len(item) == 1]
    singlequote = len(singles) / len(boundings)

    if singlequote > 0.4:  # TODO: HOLY VALUE
        return []

    buckets = linero.utils.Buckets(
        horizontals,
        selector=operator.itemgetter(3),  # y1
    )
    for cluster in clustered:
        for item in cluster:
            buckets.add(item)

    merged = [index if item else None for index, item in enumerate(buckets)]
    merged = [item for item in utila.groupby_none(merged)]

    tables = []
    for group in merged:
        if len(group) < 2:
            # TODO: MULTIPLE ITEMS IN ONLY ONE GROUP BETWEEN HORIZONTAL LINES
            continue
        topline = horizontals[group[0] - 1]
        # double content below table?
        bottomline = horizontals[min((group[-1], len(horizontals) - 1))]
        table = linero.table.table_bounding((topline, bottomline))
        tables.append(table)
    return tables


# a table must have at least this amout of lines
TABLE_MIN_LINE_COUNT = configo.HV_INT_PLUS(10)

# tables are build out of vertical and horizontal lines, but only a few
# cross lines.
TABLE_MIN_HORIZONTAL_VERTICAL_LINE = configo.HV_PERCENT_PLUS(0.9)

# tables are buld ouf long lines. The average line length is used to
# exclude figures etc.
TABLE_MIN_AVG_LINE_LENGTH = configo.HV_FLOAT_PLUS(40.0)


def judge_tables(grouped):
    """This approach handles only very simple word tables, beautiful
    "latex" tables are not supported becase there are build out of
    single horizontal lines."""
    result = []
    for page, clusters in grouped:
        pageresult = iamraw.PageContentTableBounding(page=page)
        for item in clusters:
            if len(item) < TABLE_MIN_LINE_COUNT:
                continue
            percentage = linero.lines.horiverti_percentage(item)
            if percentage < TABLE_MIN_HORIZONTAL_VERTICAL_LINE:
                continue
            avg = linero.lines.length_avg(item)
            if avg < TABLE_MIN_AVG_LINE_LENGTH:
                continue
            bounding = linero.table.table_bounding(item)
            pageresult.append(
                iamraw.TableBounding(
                    bounding=bounding,
                    lines=item,
                ))
        if not pageresult:
            continue
        result.append(pageresult)
    return result


def locate_tables(lines):
    result = []
    for page in lines:
        content = page.content
        # TODO: profile only on --profile
        # with utila.profile():
        # #  clustered = devide(content)
        clustered = devide(content)
        result.append((page.page, clustered))
    return result


def chunks(items, size: int = 1):
    result = []
    for index in range(math.ceil(len(items) / size)):
        result.append(items[index * size:(index + 1) * size])
    return result


def devide(items):
    chunk_size = 50
    splitted = chunks(items, chunk_size)
    pre = []
    for chunk in splitted:
        clustered = linero.cluster.run(chunk)
        pre.extend(clustered)
    result = linero.cluster.run(pre)
    return result
