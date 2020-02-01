# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import pytest
import utila
from iamraw import Weight
from serializeraw import load_font_content
from serializeraw import load_font_header
from yaml import FullLoader
from yaml import load

from rawmaker.features import extract_content
from rawmaker.features.fonts import FontStore
from rawmaker.features.fonts import font_fromraw
from rawmaker.features.fonts import process_page
from rawmaker.features.fonts import work
from rawmaker.reader import read
from tests.resources import HOW_TO_CPORTING_PDF
from tests.resources import INCREASING_FONT_A4
from tests.resources import TOC_PDF as RESTRUCT_FONT_MINING
from tests.resources import TWINE_PDF


def test_mining_fonts(testdir):
    header, content = work(TWINE_PDF)

    assert len(header) > 100
    assert len(content) > 300

    utila.file_create('header.yaml', header)
    utila.file_create('content.yaml', content)


def test_mining_fonts_cporting(testdir):
    header, content = work(HOW_TO_CPORTING_PDF)
    # XXX: Define good numbers
    assert len(header) > 100
    assert len(content) > 200


def test_minining_fonts_cporting_first_page():
    """Mine the first font of the document at the first page"""
    # TODO: Test mining last font of document
    with read(HOW_TO_CPORTING_PDF) as pdf:
        document = extract_content(pdf)

    fontstore = FontStore(font_fromraw)
    first_page = document[0]
    fonts = process_page(first_page, fontstore)
    assert fonts

    first_font_page = fonts[0]
    first_font = first_font_page[0]
    first_font_key = first_font[3]
    first_font_scale = fontstore.font(first_font_key).scale

    # TODO: REMOVE AFTER CLARIFING FONT PARSER
    first_font_expected = round(24.7871 / 1.34005)

    assert first_font_scale == first_font_expected


def test_mining_increasing_fonts():
    """The example contains the same sentences in fontsizes(8pt - 20pt)"""
    result = work(INCREASING_FONT_A4)
    header, _ = result

    font_sizes = [
        item['font']['scale'] for item in load(header, Loader=FullLoader)
    ]
    font_sizes = font_sizes[0:-1]  # remove the last one(page number)

    increases = [
        first < second
        for (first, second) in zip(font_sizes[0:-1], font_sizes[1:])
    ]
    assert all(increases), str(font_sizes)

    expected_fontsizes = list(range(8, 21))
    assert font_sizes == expected_fontsizes


@pytest.fixture
def restructed_fonts():
    result = work(RESTRUCT_FONT_MINING)
    header, content = load_font_header(result[0]), load_font_content(result[1])
    return header, content


def test_mining_fonts_restruct_page_5(restructed_fonts):  # pylint:disable=W0621
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
    header = {hash(font): font for font in header}
    fifths_page, _ = fifths_page
    result = [header[fontid].weight for _, __, ___, fontid in fifths_page]

    assert result == expected


@pytest.mark.parametrize('font, scale, expected_name', [
    ('WTUVLZ + NimbusRomNo9L - Regu', 9.60, 'NimbusRomNo9L'),
    ('CGWFDF + NimbusRomNo9L - ReguItal', 11.90, 'NimbusRomNo9L'),
    ('GAGKNR + NimbusRomNo9L - Medi', 13.00, 'NimbusRomNo9L'),
    ('ZTJCPR + NimbusRomNo9L - MediItal', 11.50, 'NimbusRomNo9L'),
    ('CHABPE + TimesNewRomanPSMT', 14.40, 'TimesNewRomanPSMT'),
    ('TimesNewRomanPS - ItalicMT', 13.30, 'TimesNewRomanPS-ItalicMT'),
    ('LGAZPG + SegoeUI, Bold', 27.50, 'SegoeUI'),
    ('ALONFR + SegoeUI', 13.10, 'SegoeUI'),
    ('Helvetica - Bold', 16.70, 'Helvetica-Bold'),
    ('Times - Roman', 13.40, 'Times-Roman'),
    ('CIDFont+F1', 6.60, 'F1'),
    ('Arial,Bold', 15.00, 'Arial'),
    ('ABCDEE + Verdana,Bold', 15.00, 'Verdana'),
    ('AIDZQU+Times-Roman', 13.00, 'Times-Roman'),
    ('KCXMNX+TeX-feymr10', 10.00, 'TeX-feymr10'),
])
def test_convert_font_from_raw(font, scale, expected_name):
    parsed = font_fromraw(font, scale)

    assert parsed

    assert '+' not in parsed.name, str(parsed)
    assert ',' not in parsed.name, str(parsed)

    assert expected_name == parsed.name, str(expected_name)
