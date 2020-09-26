# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila


def same_line_cluster(
        todo,
        max_diff: float = 10.0,
        min_elements: int = 1,
        matcher: callable = None,
):
    """\
    >>> len(same_line_cluster([(0, 50, 100, 55), (70, 49, 140, 52), (0, 400, 100, 401)]))
    2
    """
    if not matcher:
        matcher = lambda bounding: bounding[3]

    def classifier(candidat, clusteritem):
        return utila.near(
            matcher(candidat),
            matcher(clusteritem),
            diff=max_diff,
        )

    return utila.determine_cluster(todo, classifier, min_elements=min_elements)


utila.same_line_cluster = same_line_cluster
