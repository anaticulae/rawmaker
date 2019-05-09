# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pytest import fixture

from rawmaker import read
from rawmaker.features.border import determine_bounding_box
from tests.resource import DOCUMENTATION_TWINE_PAGES
from tests.resource import DOCUMENTATION_TWINE_PDF
from tests.resource import VIM_GUIDE_PAGES
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
