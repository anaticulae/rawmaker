# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pytest import fixture
from pytest import mark

from rawmaker.features.border import determine_boundingboxes
from rawmaker.reader import read
from rawmaker.utils import tomilimeter
from rawmaker.utils import topixel
from tests.resources import DOCUMENTATION_TWINE_PAGES
from tests.resources import DOCUMENTATION_TWINE_PDF
from tests.resources import INCREASING_FONT_A3
from tests.resources import INCREASING_FONT_A4
from tests.resources import INCREASING_FONT_A5


@fixture
def boxdata_from_pdf():
    with read(DOCUMENTATION_TWINE_PDF) as pdf:
        sizeandborders, boxes = determine_boundingboxes(pdf)
    assert sizeandborders
    assert len(sizeandborders) == DOCUMENTATION_TWINE_PAGES

    return sizeandborders, boxes


def test_border_work(boxdata_from_pdf):  #pylint:disable=W0621
    assert len(boxdata_from_pdf) == 2


def test_maximize_bounding_box(boxdata_from_pdf):  #pylint:disable=W0621
    # TODO: Remove this test?
    pageandborders, _ = boxdata_from_pdf
    assert pageandborders
    assert len(pageandborders) == DOCUMENTATION_TWINE_PAGES


@mark.parametrize(
    'increasing_fonts, expected_size_in_mm', [
        (INCREASING_FONT_A3, (297, 420)),
        (INCREASING_FONT_A4, (210, 297)),
        (INCREASING_FONT_A5, (148, 210)),
    ],
    ids=[
        'A3',
        'A4',
        'A5',
    ])
def test_page_size(increasing_fonts, expected_size_in_mm):
    with read(increasing_fonts) as pdf:
        sizeandborders, _ = determine_boundingboxes(pdf)
    size = sizeandborders[0].size  # First page

    assert tomilimeter(*size) == expected_size_in_mm

    assert topixel(*tomilimeter(*size)) == tuple([round(item) for item in size])
