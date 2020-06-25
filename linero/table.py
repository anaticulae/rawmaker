# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

TABLE_MIN_HEIGHT = 50  # TODO: HOLY VALUE
MAX_SINGLE_LINE_QUOTE = 0.2


def valid_table(bounding, navigator) -> bool:
    top, bottom = bounding[1], bounding[3]

    height = bottom - top
    if height < TABLE_MIN_HEIGHT:
        # remove to small tables
        return False

    table_content = navigator.between(
        top / navigator.height,
        bottom / navigator.height,
    )
    if not table_content:
        # no content in table
        return False

    boundings = [item.bounding for item in table_content]
    clustered = utila.same_line_cluster(
        boundings,
        min_elements=1,
    )
    singles = len([item for item in clustered if len(item) == 1])
    single_quote = singles / len(clustered)
    if singles >= 2 and single_quote > MAX_SINGLE_LINE_QUOTE:
        # invalid table content
        return False

    # table seems to be valid
    return True


def table_bounding(items):
    """Maxmize bounding"""
    x0, y0, x1, y1 = utila.INF, utila.INF, -utila.INF, -utila.INF
    for xx0, yy0, xx1, yy1 in items:
        x0 = min((x0, xx0))
        y0 = min((y0, yy0))
        x1 = max((x1, xx1))
        y1 = max((y1, yy1))
    return x0, y0, x1, y1
