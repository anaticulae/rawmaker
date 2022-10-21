# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Boxes
=====
"""

import functools
import operator

import configo
import iamraw
import pdfminer.layout
import serializeraw
import utila

# width of box
RECTANGLE_WIDTH_MIN = configo.HV_FLOAT_PLUS(default=50.0)
# height of box
RECTANGLE_HEIGHT_MIN = configo.HV_FLOAT_PLUS(default=50.0)
# distance of two merging boxes/rectangles
ENDING_DISTANCE_MAX = configo.HV_FLOAT_PLUS(default=3)


def work(lines: str, pages: tuple) -> str:
    """Extract content boxes from given `document`.

    Args:
        lines(str): path to lines
        pages(tuple): pages to analyze
    Returns:
        dumped parsed boxes, dumped parsed horizontals
    """
    assert isinstance(lines, str), type(lines)
    lines = serializeraw.load_lines(lines, pages=pages)
    boxes = determine_clusteritem(lines, determine_pageboxes)
    dumped_boxes = serializeraw.dump_boxes(boxes)
    return dumped_boxes


def determine_boxes(
    lines,
    rectangle_width_min=RECTANGLE_WIDTH_MIN,
    rectangle_height_min=RECTANGLE_HEIGHT_MIN,
):
    collect = functools.partial(
        determine_pageboxes,
        rectangle_width_min=rectangle_width_min,
        rectangle_height_min=rectangle_height_min,
    )
    boxes = determine_clusteritem(lines, collect)
    return boxes


def determine_clusteritem(
    lines: iamraw.PageContentLines,
    collector: callable,
):
    result = []
    for paged in lines:
        lines_in_page, page = paged.content, paged.page
        # remove lines which are to short and represent a dot
        lines_in_page = [
            item for item in lines_in_page if not utila.isdot(item)
        ]
        # remove duplicated lines
        lines_in_page = utila.unique_lines(lines_in_page)
        grouped = determine_cluster(lines_in_page)
        collected = collector(
            grouped,
            page,
            rotated=paged.rotated,
        )
        result.append(collected)
    return result


def determine_pageboxes(
    clusters: list[pdfminer.layout.LTLine],
    page: int,
    rotated: bool = False,  # pylint:disable=W0613
    rectangle_width_min=RECTANGLE_WIDTH_MIN,
    rectangle_height_min=RECTANGLE_HEIGHT_MIN,
) -> iamraw.PageContentBoxes:
    result = []
    for cluster in clusters:
        count = len(cluster)
        if count != 4:
            continue
        x0 = min([line[0] for line in cluster] + [line[2] for line in cluster])
        x1 = max([line[0] for line in cluster] + [line[2] for line in cluster])
        y0 = min([line[1] for line in cluster] + [line[3] for line in cluster])
        y1 = max([line[1] for line in cluster] + [line[3] for line in cluster])
        width, height = x1 - x0, y1 - y0
        if width < rectangle_width_min:
            # small boxes are mostly a result of bad parsed figures or
            # tables, we do not want them.
            continue
        if height < rectangle_height_min:
            continue
        box = iamraw.Box(box=iamraw.BoundingBox(x0, y0, x1, y1))
        result.append(box)
        # ensure to sort items top to bottom and left to right
        result = sorted(result, key=operator.attrgetter('box.y0', 'box.x0'))
    return iamraw.PageContentBoxes(content=result, page=page)


def determine_cluster(items: iamraw.BoundingBoxes) -> iamraw.BoundingBoxes:  # pylint:disable=R1260
    # TODO: REPLACE THIS CODE
    if not items:
        return []
    # a single element is a cluster
    result = [[item] for item in items]

    def match(result, current):
        for clusterindex, cluster in enumerate(result):
            for clusteritem in cluster:
                for test in current:
                    if utila.intersecting_ending(
                            clusteritem,
                            test,
                            tol=ENDING_DISTANCE_MAX,
                    ):
                        return clusterindex
        return None

    def cluster(result):
        result, todo = result[0], result[1:]
        if not isinstance(result[0], list):
            result = [result]
        while todo:  # pylint:disable=W0149
            current = todo.pop()
            index = match(result, current)
            if index is None:
                # No match, create new cluster
                result.insert(0, current)
            else:
                result[index].extend(current)
        return result

    single = utila.Single()
    while True:  # pylint:disable=W0149
        # Break when cluster does not change result Cluster till cluster
        # move does not change the result.
        result = cluster(result)
        if single.contains(result):
            break
    return result
