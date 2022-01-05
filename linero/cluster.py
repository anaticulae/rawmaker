# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import utila.math.line


def run(lines: iamraw.BoundingBoxes, maxdiff=5.0) -> iamraw.BoundingBoxes:  # pylint:disable=R1260
    # TODO: REDUCE COPY AND PASTE
    # TODO: VERY SLOW
    if not lines:
        return []

    # a single element is a cluster
    result = [item if isinstance(item, list) else [item] for item in lines]

    def match(result, current):
        for clusterindex, cluster in enumerate(result):
            for clusteritem in cluster:
                for test in current:
                    try:
                        if not utila.math.line.intersecting_lines(
                                clusteritem,
                                test,
                                max_diff=maxdiff,
                        ):
                            continue
                    except utila.math.line.IndenticalLineError:
                        return clusterindex
                    return clusterindex
        return None

    def cluster(result):
        result, todo = result[0], result[1:]
        if not isinstance(result[0], list):
            result = [result]
        while todo:
            current = todo.pop()
            index = match(result, current)
            if index is None:
                # No match, create new cluster
                result.insert(0, current)
            else:
                result[index].extend(current)
        return result

    # Break when cluster does not change result
    # Cluster till cluster move does not change the result
    before = set()
    while True:
        result = cluster(result)
        hashid = hash(str(result))
        if hashid in before:
            break
        before.add(hashid)
    return result
