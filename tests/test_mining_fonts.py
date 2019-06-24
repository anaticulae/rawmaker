# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pytest import mark
from utila import file_create
from yaml import FullLoader
from yaml import load

from rawmaker.features.fonts import FontStore
from rawmaker.features.fonts import font_fromraw
from rawmaker.features.fonts import parse_document
from rawmaker.features.fonts import process_page
from rawmaker.features.fonts import work
from rawmaker.reader import read
from tests.resource import DOCUMENTATION_TWINE_PDF
from tests.resource import HOW_TO_CPORTING_PDF
from tests.resource import INCREASING_FONT_A4


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


@mark.xfail()
def test_mining_increasing_fonts():
    # TODO: Investiga later
    with read(INCREASING_FONT_A4) as pdf:
        result = work(pdf)
        header, content = result['header'], result['content']

    for item in load(header, Loader=FullLoader):
        # print(item['font']['scale'])
        # print(round(item['font']['scale'] - 3.15))
        print('%0.0f' % (item['font']['scale'] - 3.1))
    assert 0
