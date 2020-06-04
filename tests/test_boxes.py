# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import pytest
import utila

import rawmaker.features.border
import rawmaker.features.boxes
import rawmaker.features.horizontals
import rawmaker.features.line
import rawmaker.reader
import tests.resources
from tests.resources import HOW_TO_CPORTING_BOX_COUNT as BOX_COUNT
from tests.resources import HOW_TO_CPORTING_HORIZONTAL_COUNT as LINES_COUNT
from tests.resources import HOW_TO_CPORTING_PDF as TEST_DOCUMENT


@pytest.fixture
def linecluster():
    result = []
    with rawmaker.reader.read(TEST_DOCUMENT) as doc:
        parsed = rawmaker.features.line.lines(doc)
        size = rawmaker.features.border.pagesizes(doc)[0].size
        for pagelines, _ in parsed:
            cluster = rawmaker.features.boxes.determine_cluster(pagelines)
            result.append(cluster)
    assert result
    return result, size


def test_determine_boxes(linecluster):  # pylint:disable=W0621
    linecluster, _ = linecluster
    result = []
    for index, page in enumerate(linecluster):
        boxes = rawmaker.features.boxes.determine_pageboxes(page, index)
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
        iamraw.BoundingBox.from_list([68.812, 673.773, 68.812, 715.616]),
        iamraw.BoundingBox.from_list([543.188, 673.773, 543.188, 715.616]),
        iamraw.BoundingBox.from_list([68.613, 715.816, 543.387, 715.816]),
        iamraw.BoundingBox.from_list([68.613, 673.574, 543.387, 673.574]),
        iamraw.BoundingBox.from_list([68.812, 83.267, 68.812, 447.900]),
        iamraw.BoundingBox.from_list([543.188, 83.267, 543.188, 447.900]),
        iamraw.BoundingBox.from_list([68.613, 448.099, 543.387, 448.099]),
        iamraw.BoundingBox.from_list([68.613, 83.068, 543.387, 83.068]),
    ]
    result = rawmaker.features.boxes.determine_cluster(example)
    assert len(result) == 2

    assert len(result[0]) == 4
    assert len(result[1]) == 4


def test_determine_single_cluster():
    single = [
        iamraw.BoundingBox.from_list([68.812, 673.773, 68.812, 715.616]),
    ]
    result = rawmaker.features.boxes.determine_cluster(single)
    assert len(result) == 1
    assert len(result[0]) == 1


def test_determine_horizontal_lines(linecluster):  # pylint:disable=W0621
    linecluster, size = linecluster
    pagewidth = size.width
    document_lines = []
    for index, page in enumerate(linecluster):
        horizontal = rawmaker.features.horizontals.determine_pagehorizontals(
            cluster=page,
            page=index,
            page_width=pagewidth,
        )
        document_lines.extend(horizontal.content)
    assert len(document_lines) == LINES_COUNT


def test_determine_textboxes():
    boxes = None
    with rawmaker.reader.read(TEST_DOCUMENT) as doc:
        boxes = rawmaker.features.boxes.determine_boxes(doc)
    # flatten boxes to compute box count of document
    boxes = [page.content for page in boxes]
    count = sum([len(item) for item in boxes])
    assert count == BOX_COUNT


def test_boxes_determine_horizontals_master72pages():
    horizontals = None
    with rawmaker.reader.read(tests.resources.MASTER72) as doc:
        horizontals = rawmaker.features.horizontals.determine_horizontal(
            doc,
            tuple(range(10)),
        )

    # flatten boxes to compute horizontal count of document
    horizontals = [item.content for item in horizontals if item.content]
    horizontals = utila.flatten(horizontals)
    assert len(horizontals) == 6, horizontals
    yvalue = [item.box.y0 for item in horizontals]
    expected = [405, 690, 714, 740, 720, 760]
    assert all((item >= exp for item, exp in zip(yvalue, expected))), yvalue


def test_boxes_determine_boxes_bachelor56_titlepage():
    firstpage = (0,)
    with rawmaker.reader.read(tests.resources.BACHELOR56) as doc:
        pages = rawmaker.features.boxes.determine_boxes(doc, firstpage)
        boxes = pages[0].content

    assert len(boxes) == 1, str(boxes)
