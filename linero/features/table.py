# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""

TODO: MOVE TO LINTER

Some tables contains double lines which indicates that is something wrong.

Example:

    If you add in word a table line and do not add any content add minize the
    height of the line with your cursor.
    Indicates that table are styled different.

"""
import math

import iamraw
import serializeraw
import utila

import linero.cluster
import linero.lines


def work(lines: str, pages: tuple = None) -> str:
    loaded = serializeraw.load_lines(lines, pages=pages)

    grouped = locate_tables(loaded)
    result = judge_tables(grouped)

    dumped = serializeraw.dump_tables(result)
    return dumped


def table_bounding(items):
    """Maxmize bounding"""
    x0, y0, x1, y1 = utila.INF, utila.INF, -utila.INF, -utila.INF
    for xx0, yy0, xx1, yy1 in items:
        x0 = min((x0, xx0))
        y0 = min((y0, yy0))
        x1 = max((x1, xx1))
        y1 = max((y1, yy1))
    return x0, y0, x1, y1


def judge_tables(grouped):
    """This approach handles only very simple word tables, beautiful
    "latex" tables are not supported becase there are build out of
    single horizontal lines."""
    result = []
    for page, clusters in grouped:
        pageresult = iamraw.PageContentTableBounding(page=page)
        for item in clusters:
            if len(item) < 10:  # TODO: HOLY VALUE
                continue
            percentage = linero.lines.horiverti_percentage(item)
            if percentage < 0.9:  # TODO: HOLY VALUE
                continue
            avg = linero.lines.length_avg(item)
            if avg < 40.0:  # TODO: HOLY VALUE
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
        with utila.profile():
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
