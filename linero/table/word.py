# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import math

import configo
import iamraw
import utila

import linero.cluster
import linero.lines
import linero.table

# a table must have at least this amout of lines
TABLE_MIN_LINE_COUNT = configo.HV_INT_PLUS(10)

# tables are build out of vertical and horizontal lines, but only a few
# cross lines.
TABLE_MIN_HORIZONTAL_VERTICAL_LINE = configo.HV_PERCENT_PLUS(0.9)


@utila.profile('strategy:word')
def run(lines):
    grouped = locate_tables(lines)
    result = judge_tables(grouped)
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
            if avg < linero.table.TABLE_MIN_AVG_LINE_LENGTH:
                continue
            bounding = utila.rectangle_max(item)
            pageresult.append(
                iamraw.TableBounding(
                    bounding=bounding,
                    lines=item,
                ))
        result.append(pageresult)
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
