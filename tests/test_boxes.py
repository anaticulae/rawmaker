# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from iamraw.document.utils import BoundingBox
from pytest import fixture

from rawmaker.features.boxes import bounding
from rawmaker.features.boxes import determine_boxes
from rawmaker.features.boxes import determine_cluster
from rawmaker.features.boxes import determine_horizontal_lines
from rawmaker.features.boxes import determine_textboxes
from rawmaker.features.boxes import intersecting_lines
from rawmaker.features.boxes import lines
from rawmaker.reader import read
from tests.resource import HOW_TO_CPORTING_BOX_COUNT as BOX_COUNT
from tests.resource import HOW_TO_CPORTING_HORIZONTAL_COUNT as LINES_COUNT
from tests.resource import HOW_TO_CPORTING_PDF as TEST_DOCUMENT


@fixture
def linecluster():
    result = []
    with read(TEST_DOCUMENT) as doc:
        parsed = lines(doc)
        for page in parsed:
            cluster = determine_cluster(bounding(page))
            result.append(cluster)
    assert result
    return result


def test_determine_boxes(linecluster):  # pylint:disable=W0621
    result = []
    for page in linecluster:
        boxes = determine_boxes(page)
        result.extend(boxes)
    # single raw box in document, the rest is rect
    assert len(result) == BOX_COUNT


def test_determine_cluster_per_pages(linecluster):  # pylint:disable=W0621
    expected = [4, 2, 2, 1, 1, 1, 1, 1, 0]
    for index, item in enumerate(linecluster):
        assert len(item) == expected[index], 'Page %d' % index


def test_determine_clusters():
    example = [
        BoundingBox.from_list([68.812, 673.773, 68.812, 715.616]),
        BoundingBox.from_list([543.188, 673.773, 543.188, 715.616]),
        BoundingBox.from_list([68.613, 715.816, 543.387, 715.816]),
        BoundingBox.from_list([68.613, 673.574, 543.387, 673.574]),
        BoundingBox.from_list([68.812, 83.267, 68.812, 447.900]),
        BoundingBox.from_list([543.188, 83.267, 543.188, 447.900]),
        BoundingBox.from_list([68.613, 448.099, 543.387, 448.099]),
        BoundingBox.from_list([68.613, 83.068, 543.387, 83.068]),
    ]
    result = determine_cluster(example)
    assert len(result) == 2

    assert len(result[0]) == 4
    assert len(result[1]) == 4


def test_determine_single_cluster():
    single = [
        BoundingBox.from_list([68.812, 673.773, 68.812, 715.616]),
    ]
    result = determine_cluster(single)
    assert len(result) == 1
    assert len(result[0]) == 1


def test_determine_horizontal_lines(linecluster):  # pylint:disable=W0621
    document_lines = []
    for page in linecluster:
        horizontal = determine_horizontal_lines(page)
        document_lines.extend(horizontal)
    assert len(document_lines) == LINES_COUNT


def test_determine_textboxes():
    boxes = None
    with read(TEST_DOCUMENT) as doc:
        boxes = determine_textboxes(doc)
    assert boxes
    assert len(boxes) == BOX_COUNT


def test_intersecting_lines():
    horizontal = (5, 0, 10, 0)
    vertical = (10, 0, 10, 30)
    intersected = intersecting_lines(horizontal, vertical)
    assert intersected
