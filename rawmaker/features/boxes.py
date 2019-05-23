# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
from dataclasses import dataclass
from math import sqrt
from typing import List

from iamraw import BoundingBox
# TODO: Update after upgrade utila
from iamraw.document.utils import Boxed
from pdfminer.layout import LTLine
from pdfminer.layout import LTRect
from pdfminer.pdfdocument import PDFDocument
from utila import Flag
from utila import logging
from utila import logging_error

from rawmaker.features import process_pagecontent


# TODO: Remove after upgrading iamraw
@classmethod
def from_list(cls, data):
    """Create Box from list"""
    return cls(
        x_bottom=data[0],
        y_bottom=data[1],
        x_top=data[2],
        y_top=data[3],
    )


BoundingBox.from_list = from_list


def work(document: PDFDocument):
    return {'feature_box': ''}


# TODO: Move to iamraw
@dataclass
class HorizontalLine(Boxed):

    @property
    def width(self):
        return abs(self.box.x1 - self.box.x0)


@dataclass
class Box(Boxed):
    # TODO: Textbox?
    pass


def determine_boxes(document: PDFDocument):
    return determine_clusteritem(document, determine_pageboxes)


def determine_horizontal(document: PDFDocument):
    return determine_clusteritem(document, determine_pagehorizontal)


def determine_clusteritem(document: PDFDocument, collector: callable):
    result = []
    document_lines = lines(document)
    for lines_in_page in document_lines:
        lines_in_page = bounding(lines_in_page)
        grouped = determine_cluster(lines_in_page)
        boxes = collector(grouped)
        result.append(boxes)
    return result


def determine_pageboxes(cluster: List[LTLine]):
    result = []
    for item in cluster:
        count = len(item)
        if count != 4:
            continue

        x0 = min([min(line[0], line[2]) for line in item])
        y0 = min([min(line[1], line[3]) for line in item])
        x1 = max([max(line[0], line[2]) for line in item])
        y1 = max([max(line[1], line[3]) for line in item])

        box = Box(box=BoundingBox.from_list([x0, y0, x1, y1]))
        result.append(box)
        logging('Box %.2f %.2f %.2f %.2f' % (x0, y0, x1, y1))
    return result


def determine_pagehorizontal(cluster: List[List[LTLine]],
                            ) -> List[HorizontalLine]:
    result = []
    for merged in cluster:
        if len(merged) != 1:
            continue
        x0, y0, x1, y1 = merged[0]
        xleft = min([x0, y1])
        height = abs(y0 - y1)
        width = abs(x0 - x1)
        if height < HORIZONTAL_MAX_ERROR and width > HORIZONTAL_MIN_WIDTH:
            logging('Horizontal %.2f %.2f width: %d' % (xleft, y0, width))
            result.append(HorizontalLine(box=BoundingBox.from_list(merged[0])))
            xleft = min([x0, x1])
        else:
            msg = 'No horizontal line %.2f %.2f %.2f %.2f' % (x0, y0, x1, y1)
            logging_error(msg)
    return result


def determine_cluster(lines: List[BoundingBox]) -> List[BoundingBox]:
    if not lines:
        return []

    # a single element is a cluster
    result = [[item] for item in lines]

    def match(result, current):
        for clusterindex, cluster in enumerate(result):
            for clusteritem in cluster:
                match = [
                    intersecting_lines(clusteritem, test) for test in current
                ]
                if any(match):
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


MIN_DISTANCE = 3


def intersecting_lines(first: BoundingBox, second: BoundingBox):
    """Check if start or end point of two line match

    Args:
        first(BoundingBox):
        second(BoundingBox):
    Returns:
        True if least one elements matches, else False
    """
    # Check only if points intersects
    x0, y0, x2, y2 = first
    x1, y1, x3, y3 = second

    first_distance = min(distance(x0, y0, x1, y1), distance(x0, y0, x3, y3))
    second_distance = min(distance(x2, y2, x3, y3), distance(x2, y2, x1, y1))
    if first_distance < 0.00001 and second_distance < 0.00001:
        # intersecting with themself
        return None

    if first_distance < MIN_DISTANCE:
        return True

    if second_distance < MIN_DISTANCE:
        return True

    return False


def bounding(items):
    """Extract boundingbox out of LT-Element"""
    result = [item.bbox for item in items]
    return result


HORIZONTAL_MAX_ERROR = 1.0
# TODO: Make dependend on page size
HORIZONTAL_MIN_WIDTH = 400


def type_in_document(document: PDFDocument, datatype):
    assert isinstance(document, PDFDocument), type(document)
    result = []
    for page in process_pagecontent(document):
        data = [item for item in page if isinstance(item, datatype)]
        result.append(data)
    return result


def lines(document: PDFDocument):
    assert isinstance(document, PDFDocument), type(document)
    return type_in_document(document, LTLine)


def distance(x0, y0, x1, y1):
    return sqrt(pow((x0 - x1), 2) + pow((y0 - y1), 2))


def commandline():
    return Flag(longcut='%s' % name(), message='Extract boxes out of document.')


def name():
    return 'boxes'
