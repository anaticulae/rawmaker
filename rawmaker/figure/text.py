# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import utila

import rawmaker.figure.utils

# TODO: REMOVE HORIZONTAL AND VERTICAL LINES TO AVOID DETECTING TABLES AS
# FIGURE?


def text_figures(items) -> iamraw.Figure:
    clustered = cluster(items)
    result = []
    for bounding in clustered:
        raw = rawmaker.figure.utils.rawfigure_frombounding(bounding)
        figure = iamraw.Figure(data=raw, bounding=bounding)
        result.append(figure)
    return result


MIN_CLUSTER_SIZE = 20


def cluster(items):
    bucket = utila.Buckets(utila.ranges(0, 1000, 50), sorting=True)
    for item in items:
        start, end = item.bbox[1], item.bbox[3]
        # left to right to ensure that line is marked more than one
        # keep y-expansion in calculation
        # for _ in utila.ranges(item.bbox[0], item.bbox[2], step=50):
        for coordinate in utila.ranges(start, end, step=5):
            bucket.add(utila.roundme(coordinate))

    content = list(bucket)
    content = merge_neighbours(content)

    selected = [set(item) for item in content if len(item) >= MIN_CLUSTER_SIZE]

    result = []
    for current in selected:
        y0 = min(current)
        y1 = max(current)
        incluster = [
            item.bbox
            for item in items
            if y0 <= item.bbox[1] <= y1 or y0 <= item.bbox[3] <= y1
        ]
        x0 = min(item[0] for item in incluster)
        x1 = max(item[2] for item in incluster)
        result.append((x0, y0, x1, y1))
    return result


def merge_neighbours(items) -> list:
    # TODO: REPLACE WITH UTILA.GROUPBY_NEIGHBORS
    if not items:
        return items
    result = []
    collected = []
    for item in items:
        if item:
            collected.extend(item)
        else:
            result.append(collected)
            collected = []
    if collected:
        result.append(collected)
    return result
