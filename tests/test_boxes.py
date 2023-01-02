# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import pytest
import serializeraw
import utila
import utilatest

import rawmaker.features.border
import rawmaker.features.boxes
import rawmaker.features.horizontals
import rawmaker.features.line
import rawmaker.reader
import tests.resources


@pytest.fixture
def linecluster():
    utilatest.fixture_requires(power.DOCU009_PDF)
    result = []
    with rawmaker.reader.read(power.DOCU009_PDF) as doc:
        parsed = rawmaker.features.line.lines(doc)
        size = rawmaker.features.border.pagesizes(doc)[0].size
        for pagelines, _ in parsed:
            cluster = rawmaker.features.boxes.determine_cluster(pagelines)
            result.append(cluster)
    assert result
    return result, size


@utilatest.longrun
def test_determine_boxes(linecluster):  # pylint:disable=W0621
    linecluster, _ = linecluster
    result = []
    for index, page in enumerate(linecluster):
        boxes = rawmaker.features.boxes.determine_pageboxes(
            page,
            index,
            rectangle_width_min=25,
            rectangle_height_min=25,
        )
        result.extend(boxes.content)
    # single raw box in document, the rest is rect
    assert len(result) == tests.resources.DOCU009_BOX_COUNT


@utilatest.longrun
def test_determine_cluster_per_pages(linecluster):  # pylint:disable=W0621
    linecluster, _ = linecluster
    expected = [4, 2, 2, 1, 1, 1, 1, 1, 0]
    for index, item in enumerate(linecluster):
        assert len(item) == expected[index], f'Page {index}'


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


@utilatest.longrun
def test_determine_horizontal_lines(linecluster):  # pylint:disable=W0621
    linecluster, size = linecluster
    pagewidth = size.width
    lines = []
    for index, page in enumerate(linecluster):
        horizontal = rawmaker.features.horizontals.determine_pagehorizontals(
            cluster=page,
            page=index,
            page_width=pagewidth,
        )
        lines.extend(horizontal.content)
    assert len(lines) == tests.resources.DOCU009_HORIZONTAL_COUNT


@utilatest.requires(power.DOCU009_PDF)
def test_determine_textboxes():
    lines = iamraw.path.line(power.link(power.DOCU009_PDF))
    lines = serializeraw.load_lines(lines)
    boxes = rawmaker.features.boxes.determine_boxes(
        lines,
        rectangle_width_min=25,
        rectangle_height_min=25,
    )
    # flatten boxes to compute box count of document
    boxes = [page.content for page in boxes]
    count = sum((len(item) for item in boxes))
    assert count == tests.resources.DOCU009_BOX_COUNT


@utilatest.requires(power.MASTER072_PDF)
def test_boxes_determine_horizontals_master72pages():
    horizontals = None
    lines = iamraw.path.line(power.link(power.MASTER072_PDF))
    lines = serializeraw.load_lines(lines, pages=utila.rtuple(0, 10))
    horizontals = rawmaker.features.horizontals.determine_horizontal(lines)
    # flatten boxes to compute horizontal count of document
    horizontals = [item.content for item in horizontals if item.content]
    horizontals = utila.flat(horizontals)
    assert len(horizontals) == 6, horizontals
    yvalue = [item.box.y0 for item in horizontals]
    expects = [410, 690, 714, 745, 725, 760]
    assert utila.nears(yvalue, expects, diff=5.0), (f'{yvalue}; {expects}')


@utilatest.requires(power.BACHELOR056_PDF)
def test_boxes_determine_boxes_bachelor56_titlepage():
    lines = iamraw.path.line(power.link(power.BACHELOR056_PDF))
    lines = serializeraw.load_lines(lines, pages=(0,))
    pages = rawmaker.features.boxes.determine_boxes(lines)
    boxes = pages[0].content
    assert len(boxes) == 1, str(boxes)
