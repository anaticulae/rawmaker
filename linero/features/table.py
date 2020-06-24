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


def work(
        text: str,
        textposition: str,
        horizontals: str,
        pages: tuple = None,
) -> str:
    horizontals = serializeraw.load_horizontals(horizontals, pages=pages)
    navigators = serializeraw.create_pagetextnavigators_fromfile(
        text,
        textposition,
        pages=pages,
    )

    result = []
    for navigator in navigators:
        pagehorizontals = utila.select_page(horizontals, page=navigator.page)
        if not pagehorizontals:
            continue
        pagehorizontals = pagehorizontals.content
        extracted = cluster_page(navigator, pagehorizontals)
        if not extracted:
            continue
        result.append(
            iamraw.PageContentTableBounding(
                page=navigator.page,
                content=extracted,
            ))
    dumped = serializeraw.dump_tables(result)
    return dumped


def cluster_page(navigator, horizontals) -> iamraw.TableBoundings:
    if len(horizontals) <= 2:
        # TODO: SINGLE LINE TABLE?
        return []

    boundings = [item.bounding for item in navigator]
    boundings = sort_leftright_topdown(boundings)
    clustered = same_line_cluster(boundings, min_elements=2)  # TODO: HOLY VALUE

    horizontals = [item.box for item in horizontals]
    buckets = Buckets(horizontals, selector=operator.attrgetter('y1'))
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
        bottomline = horizontals[min(group[-1], len(horizontals) - 1)]
        table = table_bounding((topline, bottomline))
        tables.append(table)

    # TODO: ADD LINES
    result = [iamraw.TableBounding(bounding=item) for item in tables]
    return result


def table_bounding(items):
    """Maxmize bounding"""
    x0, y0, x1, y1 = utila.INF, utila.INF, -utila.INF, -utila.INF
    for xx0, yy0, xx1, yy1 in items:
        x0 = min((x0, xx0))
        y0 = min((y0, yy0))
        x1 = max((x1, xx1))
        y1 = max((y1, yy1))
    return x0, y0, x1, y1


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
            bounding = table_bounding(item)
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


def same_line_cluster(
        todo,
        max_difference: float = 10.0,
        min_elements: int = 1,
):

    def classifier(candidat, clusteritem, max_difference=max_difference):

        def matcher(candidat, clusteritem):
            diff = math.fabs(candidat.y1 - clusteritem.y1)
            return diff <= max_difference

        return matcher(candidat, clusteritem)

    return utila.determine_cluster(todo, classifier, min_elements=min_elements)


class Buckets:
    """Fill items depending on values into upper limit buckets.

    >>> bucket = Buckets((50, 100, 400), sorting=True)
    >>> for item in (70, 85, 500, 130, 100):
    ...    bucket.add(item)
    >>> list(bucket)
    [[], [70, 85], [100, 130], [500]]

    Possible selector:
        selector=operator.attrgetter('y1')
    """

    def __init__(self, border, selector=None, sorting: bool = False):
        self.sorting = sorting
        self.selector = selector if selector else lambda x: x

        self.border = [self.selector(item) for item in border]
        self.border.append(utila.INF)

        self.bucket = [[] for _ in range(len(self.border))]

    def add(self, item):
        for border, bucket in zip(self.border, self.bucket):
            if self.selector(item) >= border:
                continue
            bucket.append(item)
            return

    def __getitem__(self, index):
        data = self.bucket[index]
        if not self.sorting:
            return data
        return sorted(data, key=self.selector)


def sort_leftright_topdown(items):
    # left to right
    items = sorted(items, key=operator.itemgetter(0))
    # top down
    items = sorted(items, key=operator.itemgetter(3))
    return items
