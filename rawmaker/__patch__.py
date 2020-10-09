# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila


def intersecting_ending(first: tuple, second: tuple, tol: float = 3.0) -> bool:
    """Check if start or end point of two line intersects.

    >>> intersecting_ending((0, 0, 100, 0), (100, 0, 100, 100))
    True
    >>> intersecting_ending((33, 33, 66, 66), (66, 66, 33, 33)) is None
    True
    >>> intersecting_ending((15.0, 15.0, 30.0, 30.0), (-15.0, -15.0, -30.0, -30.0))
    False

    Args:
        first(BoundingBox): line(x0, y0, x1, y1)
        second(BoundingBox): line(x0, y0, x1, y1)
        tol(float): max distance of two matching points
    Returns:
        None  if both lines are equal
        False if nothing matches
        True  if least one element matches
    """
    # Check only if points intersects
    x0, y0, x2, y2 = first
    x1, y1, x3, y3 = second

    first_distance = min(utila.length(x0, y0, x1, y1), utila.length(x0, y0, x3, y3)) # yapf:disable
    second_distance = min(utila.length(x2, y2, x3, y3), utila.length(x2, y2, x1, y1)) # yapf: disable

    if first_distance < 0.00001 and second_distance < 0.00001:
        # intersecting with themself
        return None

    if first_distance <= tol:
        return True

    if second_distance <= tol:
        return True

    return False


utila.intersecting_ending = intersecting_ending
