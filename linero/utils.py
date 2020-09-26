# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import operator


def sort_leftright_topdown(items):
    # left to right
    items = sorted(items, key=operator.itemgetter(0))
    # top down
    items = sorted(items, key=operator.itemgetter(3))
    return items


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
