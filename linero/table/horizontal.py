# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import operator

import iamraw
import utila

import linero.lines
import linero.table
import linero.utils


def run(lines, navigators):
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
    return result


def cluster_page(navigator, lines) -> iamraw.TableBoundings:
    horizontals = [
        item for item in lines if linero.lines.horizontal(
            item,
            maxdiff=linero.table.TABLE_HORIZONTAL_MAX_DIFF,
        )
    ]

    if len(horizontals) <= 2:
        # TODO: SINGLE LINE TABLE?
        return []

    boundings = [item.bounding for item in navigator]
    boundings = linero.utils.sort_leftright_topdown(boundings)

    result = []
    grouped_horizontals = linero.table.utils.group_horizontals(horizontals)
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
            if linero.table.utils.valid_table(item, navigator)
        ]

        # merge connected tables
        tables = linero.table.utils.merge_tables(tables)

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

    buckets = utila.Buckets(
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
        table = linero.table.utils.table_bounding((topline, bottomline))
        tables.append(table)
    return tables
