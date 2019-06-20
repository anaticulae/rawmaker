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

from rawmaker import read
from rawmaker.features.border import determine_bounding_box
from rawmaker.utils import tomilimeter
from rawmaker.utils import topixel
from tests.resource import DOCUMENTATION_TWINE_PAGES
from tests.resource import DOCUMENTATION_TWINE_PDF
from tests.resource import INCREASING_FONT_A3
from tests.resource import INCREASING_FONT_A4
from tests.resource import INCREASING_FONT_A5
from tests.resource import VIM_GUIDE_PAGE_COUNT
from tests.resource import VIM_GUIDE_PDF


@fixture
def boxdata_from_pdf():
    with read(DOCUMENTATION_TWINE_PDF) as pdf:
        size, border, boxes = determine_bounding_box(pdf)
    assert size, border
    assert len(size) == DOCUMENTATION_TWINE_PAGES
    assert len(border) == DOCUMENTATION_TWINE_PAGES

    return size, border, boxes


def test_border_work(boxdata_from_pdf):  #pylint:disable=W0621
    assert len(boxdata_from_pdf) == 3


def test_maximize_bounding_box(boxdata_from_pdf):  #pylint:disable=W0621
    pagesize, border, _ = boxdata_from_pdf
    assert pagesize, border
    assert len(pagesize) == DOCUMENTATION_TWINE_PAGES
    assert len(border) == DOCUMENTATION_TWINE_PAGES


@mark.parametrize('increasing_fonts, expected_size_in_mm', [
    (INCREASING_FONT_A3, (297, 420)),
    (INCREASING_FONT_A4, (210, 297)),
    (INCREASING_FONT_A5, (148, 210)),
])
def test_page_size(increasing_fonts, expected_size_in_mm):
    with read(increasing_fonts) as pdf:
        size, _, __ = determine_bounding_box(pdf)
    size = size[0]  # First page

    assert tomilimeter(*size) == expected_size_in_mm

    assert topixel(*tomilimeter(*size)) == tuple([round(item) for item in size])
