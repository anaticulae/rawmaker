# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from iamraw import Weight
from pytest import fixture
from pytest import mark
from serializeraw import load_font_content
from serializeraw import load_font_header
from utila import file_create
from yaml import FullLoader
from yaml import load

from rawmaker.features.fonts import FontStore
from rawmaker.features.fonts import font_fromraw
from rawmaker.features.fonts import parse_document
from rawmaker.features.fonts import process_page
from rawmaker.features.fonts import work
from rawmaker.reader import read
from tests.resources import DOCUMENTATION_TWINE_PDF
from tests.resources import HOW_TO_CPORTING_PDF
from tests.resources import INCREASING_FONT_A4
from tests.resources import TOC_PDF as RESTRUCT_FONT_MINING


def test_mining_fonts(testdir):
    header, content = work(DOCUMENTATION_TWINE_PDF)

    assert len(header) > 100
    assert len(content) > 300

    file_create('header.yaml', header)
    file_create('content.yaml', content)


def test_mining_fonts_cporting(testdir):
    header, content = work(HOW_TO_CPORTING_PDF)
    # XXX: Define good numbers
    assert len(header) > 100
    assert len(content) > 200


def test_minining_fonts_cporting_first_page():
    """Mine the first font of the document at the first page"""
    # TODO: Test mining last font of document
    with read(HOW_TO_CPORTING_PDF) as pdf:
        document = parse_document(pdf)

    fontstore = FontStore(font_fromraw)
    first_page = document[0]

    fonts = process_page(first_page, fontstore)
    assert fonts

    first_font = fontstore.fonts[0].scale

    first_font_expected = round(704.02 - 668.55, 1)

    assert first_font == first_font_expected


@mark.xfail(raises=AssertionError)
def test_mining_increasing_fonts():
    """The example contains the same sentences in fontsizes(8pt - 20pt)"""
    # TODO: Improve font size detection
    result = work(INCREASING_FONT_A4)
    header, _ = result

    font_size = [
        item['font']['scale'] for item in load(header, Loader=FullLoader)
    ]
    font_size = font_size[0:-1]  # remove the last one(page number)

    increases = [
        first < second
        for (first, second) in zip(font_size[0:-1], font_size[1:])
    ]
    assert all(increases), str(font_size)

    font_size = [int(item) for item in font_size]
    expected_fontsizes = list(range(8, 21))
    assert font_size == expected_fontsizes


@fixture
def restructed_fonts():
    result = work(RESTRUCT_FONT_MINING)
    header, content = load_font_header(result[0]), load_font_content(result[1])
    return header, content


def test_mining_fonts_restruct_page_5(restructed_fonts):
    """Mine the fifths page, compare only `Weight` for not beeing to
    specific"""
    header, content = restructed_fonts
    fifths_page = content[4]

    expected = [
        Weight.BOLD,
        Weight.LIGHT,
        Weight.MEDIUM,
        Weight.LIGHT,
        Weight.MEDIUM,
        Weight.LIGHT,
        Weight.BOLD,
    ]

    result = [header[fontid].weight for _, __, ___, fontid in fifths_page]

    assert result == expected
