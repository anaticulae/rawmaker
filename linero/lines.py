# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import math
import statistics

import configo
import utila

HORIZONTAL_MAX_DIFF = configo.HV_FLOAT_PLUS(default=0.01).value

VERTICAL_MAX_DIFF = configo.HV_FLOAT_PLUS(default=0.01)


def horizontal(item: tuple) -> bool:
    """Check that difference between two line ending points is in range
    to accept as horizontal line."""
    diff = math.fabs(item[1] - item[3])
    return diff <= HORIZONTAL_MAX_DIFF


def vertical(item: tuple) -> bool:
    """Check that difference between two line ending points is in range
    to accept as vertical line."""
    diff = math.fabs(item[0] - item[2])
    return diff <= VERTICAL_MAX_DIFF


def horiverti_lines(items):
    return [item for item in items if horizontal(item) or vertical(item)]


def horiverti_percentage(items) -> float:
    if not items:
        return None
    matched = len(horiverti_lines(items))
    return len(items) / matched


def length_avg(items) -> float:
    length = [utila.length(*item) for item in items]
    mean = statistics.mean(length)
    rounded = utila.roundme(mean)
    return rounded
