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

import utila

import linero.math


def horizontal(item):
    diff = math.fabs(item[1] - item[3])
    return diff <= 0.01  # TODO: HOLY VALUE


def vertical(item):
    diff = math.fabs(item[0] - item[2])
    return diff <= 0.01  # TODO: HOLY VALUE


def horiverti_lines(items):
    return [item for item in items if horizontal(item) or vertical(item)]


def horiverti_percentage(items) -> float:
    if not items:
        return None
    matched = len(horiverti_lines(items))
    return len(items) / matched


def length_avg(items) -> float:
    length = [linero.math.length(item) for item in items]
    mean = statistics.mean(length)
    rounded = utila.roundme(mean)
    return rounded
