# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Boxes
=====
"""

import operator
import typing

import iamraw
import pdfminer.layout
import serializeraw
import utila

import rawmaker.features.line
import rawmaker.reader

# TODO: LTLine - replace with own data structure to reduce dependencies to
# rawmaker
LineClusters = typing.List[typing.List[pdfminer.layout.LTLine]]


def work(document: str, pages: tuple) -> str:
    """Extract content boxes from given `document`.

    Args:
        document(str): path to document
        pages(tuple): pages to analyze
    Returns:
        dumped parsed boxes, dumped parsed horizontals
    """
    assert isinstance(document, str), str(document)
    with rawmaker.reader.read(document) as pdf:
        boxes = determine_boxes(pdf, pages=pages)
    dumped_boxes = serializeraw.dump_boxes(boxes)
    return dumped_boxes


def determine_boxes(
        document: pdfminer.pdfdocument.PDFDocument,
        pages: tuple = None,
):
    result = determine_clusteritem(
        document,
        determine_pageboxes,
        pages=pages,
    )
    return result


def determine_clusteritem(
        document: pdfminer.pdfdocument.PDFDocument,
        collector: callable,
        pages: tuple = None,
):
    result = []
    document_lines = rawmaker.features.line.lines(document, pages=pages)

    for lines_in_page, page in document_lines:
        # remove lines which are to short and represent a dot
        lines_in_page = [
            item for item in lines_in_page if not utila.isdot(item)
        ]
        # remove duplicated lines
        lines_in_page = utila.unique_lines(lines_in_page)
        grouped = determine_cluster(lines_in_page)
        collected = collector(grouped, page)
        result.append(collected)
    return result


def determine_pageboxes(
        cluster: typing.List[pdfminer.layout.LTLine],
        page: int,
) -> iamraw.PageContentBoxes:
    result = []
    for item in cluster:
        count = len(item)
        if count != 4:
            continue

        x0 = min([min(line[0], line[2]) for line in item])
        y0 = min([min(line[1], line[3]) for line in item])
        x1 = max([max(line[0], line[2]) for line in item])
        y1 = max([max(line[1], line[3]) for line in item])

        box = iamraw.Box(box=iamraw.BoundingBox.from_list([x0, y0, x1, y1]))
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
                    if intersecting_endings(clusteritem, test):
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

    single = utila.Single()
    while True:
        # Break when cluster does not change result Cluster till cluster
        # move does not change the result.
        result = cluster(result)
        if single.contains(result):
            break
    return result


MIN_DISTANCE = 3


def intersecting_endings(
        first: iamraw.BoundingBox,
        second: iamraw.BoundingBox,
) -> bool:
    """Check if start or end point of two line match.

    Args:
        first(BoundingBox): line to cross
        second(BoundingBox): line to cross
    Returns:
        True if least one elements matches, else False
    """
    # Check only if points intersects
    x0, y0, x2, y2 = first
    x1, y1, x3, y3 = second

    first_distance = min(
        utila.length(x0, y0, x1, y1), utila.length(x0, y0, x3, y3))
    second_distance = min(
        utila.length(x2, y2, x3, y3), utila.length(x2, y2, x1, y1))
    if first_distance < 0.00001 and second_distance < 0.00001:
        # intersecting with themself
        return None

    if first_distance < MIN_DISTANCE:
        return True

    if second_distance < MIN_DISTANCE:
        return True

    return False
