# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import math

import utila

NEAR_ZERO = 0.0000001
NEAR_INF = 10.0**64


class IndenticalLineError(ValueError):
    pass


def intersecting_lines(first, second, max_diff=0.0):
    # TODO: ADD DOC HERE
    if length(first) < NEAR_ZERO or length(second) < NEAR_ZERO:
        raise ValueError(f"it's not a line it's a dot {first}; {second}")
    # TODO: REDUCE COMPLEXITY
    # TODO: MOVE TO UTIL.MATH
    # disable short math names
    # pylint:disable=C0103
    x0, y0, x1, y1 = first

    x00, y00, x11, y11 = second

    try:
        m0 = (x0 - x1) / (y0 - y1)
    except ZeroDivisionError:
        m0 = 0.0
    try:
        m1 = (x00 - x11) / (y00 - y11)
    except ZeroDivisionError:
        m1 = 0.0

    if zero(x0 - x1):
        m0 = NEAR_INF
    if zero(x00 - x11):
        m1 = NEAR_INF

    n0 = y0 - m0 * x0
    n1 = y00 - m1 * x00

    x0, x1 = min([x0, x1]), max([x0, x1])
    y0, y1 = min([y0, y1]), max([y0, y1])
    x00, x11 = min([x00, x11]), max([x00, x11])
    y00, y11 = min([y00, y11]), max([y00, y11])

    if zero(n0 - n1) and zero(m0 - m1):
        if y0 == y00 and y1 == y11:
            raise IndenticalLineError(f'identical lines {first} {second}')

    if m0 == m1 and not inf(m0):
        # 2 never matching lines
        return None
    try:
        xmatch = (n1 + n0) / (m0 - m1)
    except ZeroDivisionError:
        xmatch = None

    if not xmatch:
        if max_diff:
            potential = [
                (x0, y0, x00, y00),
                (x0, y0, x11, y11),
                (x1, y1, x00, y00),
                (x1, y1, x11, y11),
            ]
            for item in potential:
                if length(item) < max_diff:
                    return (item[0], item[1])
        return None

    ymatch = xmatch * m0 + n0
    xmatch = utila.roundme(xmatch)

    inside = all([
        -max_diff / 2 + x0 <= xmatch <= x1 + max_diff / 2,
        -max_diff / 2 + x00 <= xmatch <= x11 + max_diff / 2,
        -max_diff / 2 + y0 <= ymatch <= y1 + max_diff / 2,
        -max_diff / 2 + y00 <= ymatch <= y11 + max_diff / 2,
    ])
    if not inside:
        return None

    return xmatch, ymatch


def length(item):
    x0, y0, x1, y1 = item
    result = math.sqrt((x0 - x1)**2 + (y0 - y1)**2)
    result = utila.roundme(result)
    return result


def zero(item):
    return math.fabs(item) <= NEAR_ZERO


def inf(item):
    return math.fabs(item) >= NEAR_INF
