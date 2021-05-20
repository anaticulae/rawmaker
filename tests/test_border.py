# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utila
import utilatest

import rawmaker.features.border
import tests.resources


@pytest.fixture
def boxdata_from_pdf():
    with rawmaker.reader.read(power.DOCU35_PDF) as pdf:
        sizeandborders, boxes = rawmaker.features.border.determine_boundingboxes(
            pdf)
    assert sizeandborders
    assert len(sizeandborders) == tests.resources.TWINE_PAGES

    return sizeandborders, boxes


@utilatest.longrun
def test_border_work(boxdata_from_pdf):  #pylint:disable=W0621
    assert len(boxdata_from_pdf) == 2


@utilatest.longrun
def test_maximize_bounding_box(boxdata_from_pdf):  #pylint:disable=W0621
    # TODO: Remove this test?
    pageandborders, _ = boxdata_from_pdf
    assert pageandborders
    assert len(pageandborders) == tests.resources.TWINE_PAGES


@pytest.mark.parametrize(
    'increasing_fonts, expected_size_in_mm',
    [
        (tests.resources.INCREASING_FONT_A3, (297, 420)),
        (tests.resources.INCREASING_FONT_A4, (210, 297)),
        (tests.resources.INCREASING_FONT_A5, (148, 210)),
    ],
    ids=[
        'A3',
        'A4',
        'A5',
    ],
)
def test_page_size(increasing_fonts, expected_size_in_mm):
    with rawmaker.reader.read(increasing_fonts) as pdf:
        sizeandborders = rawmaker.features.border.determine_boundingboxes(pdf)
    size = sizeandborders[0][0].size  # First page
    assert utila.millimeters(*size, digits=0) == expected_size_in_mm

    expected = utila.roundme(size, digits=0)
    current = utila.points(*utila.millimeters(*size), digits=0)
    assert current == expected


def test_border_pagesize_both():
    pages = (0, 105)
    with rawmaker.reader.read(power.MASTER116_PDF) as pdf:
        sizeandborders, _ = rawmaker.features.border.determine_boundingboxes(
            pdf,
            pages=pages,
        )
    pagesize_0 = sizeandborders[0].size
    pagesize_105 = sizeandborders[1].size
    assert pagesize_0 != pagesize_105, 'should not be equal'


def test_border_bounding_boxes():
    """Test that coordinates are flipped like expected in our format."""
    with rawmaker.reader.read(tests.resources.HELLO_WORLD_PDF) as pdf:
        boxes = rawmaker.features.border.determine_boundingboxes(
            pdf,
            pages=(0,),
        )[1]
    assert len(boxes) == 1, boxes
    boundings = boxes[0].boundings
    ymax = max([item[1][2] for item in boundings])
    assert ymax < 450.0, f'{ymax} was not flipped'


def test_border_pagesize_bachelor76_top_regression():
    """The pdf printer produces a white space in every header. Therefore
    the border is to near to the top. This test ensures, that
    white spaces are not part of bounding detecting."""
    with rawmaker.reader.read(power.BACHELOR076_PDF) as pdf:
        sizeandborders, _ = rawmaker.features.border.determine_boundingboxes(
            pdf,
            pages=(1,),
        )
    first = sizeandborders[0].border
    assert first.top > 70.0
