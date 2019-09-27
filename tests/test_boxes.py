# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import utila
from iamraw import BoundingBox
from pytest import fixture

import rawmaker.features.boxes
import tests.resources
from rawmaker.features.border import pagesizes
from rawmaker.features.boxes import bounding
from rawmaker.features.boxes import determine_boxes
from rawmaker.features.boxes import determine_cluster
from rawmaker.features.boxes import determine_pageboxes
from rawmaker.features.boxes import determine_pagehorizontals
from rawmaker.features.boxes import intersecting_lines
from rawmaker.features.boxes import lines
from rawmaker.features.boxes import pagesize
from rawmaker.reader import read
from tests.resources import HOW_TO_CPORTING_BOX_COUNT as BOX_COUNT
from tests.resources import HOW_TO_CPORTING_HORIZONTAL_COUNT as LINES_COUNT
from tests.resources import HOW_TO_CPORTING_PDF as TEST_DOCUMENT


@fixture
def linecluster():
    result = []
    with read(TEST_DOCUMENT) as doc:
        parsed = lines(doc)
        size = pagesizes(doc)[0].size
        for pagelines, _ in parsed:
            cluster = determine_cluster(bounding(pagelines))
            result.append(cluster)
    assert result
    return result, size


def test_determine_boxes(linecluster):  # pylint:disable=W0621
    linecluster, _ = linecluster
    result = []
    for index, page in enumerate(linecluster):
        boxes = determine_pageboxes(page, index)
        result.extend(boxes.content)
    # single raw box in document, the rest is rect
    assert len(result) == BOX_COUNT


def test_determine_cluster_per_pages(linecluster):  # pylint:disable=W0621
    linecluster, _ = linecluster
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
    linecluster, size = linecluster
    pagewidth = size.width
    document_lines = []
    for index, page in enumerate(linecluster):
        horizontal = determine_pagehorizontals(
            cluster=page,
            page=index,
            page_width=pagewidth,
        )
        document_lines.extend(horizontal.content)
    assert len(document_lines) == LINES_COUNT


def test_determine_textboxes():
    boxes = None
    with read(TEST_DOCUMENT) as doc:
        boxes = determine_boxes(doc)
    # flatten boxes to compute box count of document
    boxes = [page.content for page in boxes]
    count = sum([len(item) for item in boxes])
    assert count == BOX_COUNT


def test_intersecting_lines():
    horizontal = (5, 0, 10, 0)
    vertical = (10, 0, 10, 30)
    intersected = intersecting_lines(horizontal, vertical)
    assert intersected


@pytest.mark.xfail(reason='could not detect _________ as horizontal line')
def test_boxex_determine_horizontals_master72pages():
    horizontals = None
    with read(tests.resources.MASTER_72_NOIMAGES_TOC) as doc:
        horizontals = rawmaker.features.boxes.determine_horizontal(
            doc,
            list(range(0, 10)),
        )

    # flatten boxes to compute horizontal count of document
    horizontals = [item.content for item in horizontals if item.content]
    assert len(horizontals) == 6, horizontals
