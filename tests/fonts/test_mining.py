# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import operator

import iamraw
import power
import pytest
import serializeraw
import utila
import utilatest

import rawmaker
import rawmaker.features
import rawmaker.features.fonts
import rawmaker.fonts.parser
import rawmaker.reader
import tests
import tests.resources


@pytest.mark.usefixtures('testdir')
@utilatest.longrun
def test_mining_fonts():
    header, content = rawmaker.features.fonts.work(power.DOCU035_PDF)
    assert len(header) > 100
    assert len(content) > 300
    utila.file_create('header.yaml', header)
    utila.file_create('content.yaml', content)


@utilatest.longrun
def test_mining_fonts_cporting():
    header, content = rawmaker.features.fonts.work(power.DOCU009_PDF)
    # XXX: Define good numbers
    assert len(header) > 100
    assert len(content) > 200


@utilatest.longrun
def test_minining_fonts_cporting_first_page():
    """Mine the first font of the document at the first page"""
    # TODO: Test mining last font of document
    with rawmaker.reader.read(power.DOCU009_PDF) as pdf:
        document = rawmaker.features.extract_content(pdf)

    fontstore = rawmaker.features.fonts.FontStore(rawmaker.fonts.parser.font_fromraw) # yapf:disable
    first_page = document[0]
    fonts = rawmaker.features.fonts.process_page(first_page, fontstore)
    assert fonts

    first_font_page = fonts[0]
    first_font = first_font_page[0]
    first_font_key = first_font[3]
    first_font_scale = fontstore.font(first_font_key).scale
    # TODO: REMOVE AFTER CLARIFING FONT PARSER
    first_font_expected = utila.roundme(24.7871 / 1.34005)
    assert first_font_scale == first_font_expected


def test_minining_fonts_rise():
    """Ensure that that flip works correctly.

    There was a problem that only the chars till the first VirtualChar
    was flipped correctly. This was an effect cause VirtualChars have no
    BoundingBox.
    """
    with rawmaker.reader.read(power.DOCU009_PDF) as pdf:
        document = rawmaker.features.extract_content(pdf)
    first_page = document[0]
    no_rise = first_page[0][0][-1]
    assert no_rise.rise == 0.0, str(no_rise)  # pylint:disable=C2001


def test_mining_increasing_fonts():
    """The example contains the same sentences in font sizes(8pt - 20pt)."""
    result = rawmaker.features.fonts.work(tests.resources.INCREASING_FONT_A4)
    header, _ = result

    font_sizes = [item['font']['scale'] for item in utila.yaml_load(header)]
    font_sizes = font_sizes[0:-1]  # remove the last one(page number)

    increases = [
        first < second
        for (first, second) in zip(font_sizes[0:-1], font_sizes[1:])
    ]
    assert all(increases), str(font_sizes)

    expected_fontsizes = list(range(8, 21))
    font_sizes = utila.roundme(font_sizes, digits=0)
    assert font_sizes == expected_fontsizes


@utilatest.longrun
def test_mining_fonts_restruct_page_5():
    """Mine the fifths page, compare only `Weight` for not being to
    specific."""
    header, content = rawmaker.features.fonts.work(power.DOCU027_PDF)
    header = serializeraw.load_font_header(header)
    content = serializeraw.load_font_content(content)
    fifths_page = content[4]

    expected = [
        iamraw.Weight.BOLD,
        iamraw.Weight.LIGHT,
        iamraw.Weight.MEDIUM,
        iamraw.Weight.LIGHT,
        iamraw.Weight.MEDIUM,
        iamraw.Weight.LIGHT,
        iamraw.Weight.BOLD,
    ]
    header = {hash(font): font for font in header}
    fifths_page, _ = fifths_page
    result = [header[fontid].weight for _, __, ___, fontid in fifths_page]

    assert result == expected


@pytest.mark.font
@pytest.mark.parametrize('font, scale, expected_name', [
    ('WTUVLZ + NimbusRomNo9L - Regu', 9.60, 'NimbusRomNo9L'),
    ('CGWFDF + NimbusRomNo9L - ReguItal', 11.90, 'NimbusRomNo9L'),
    ('GAGKNR + NimbusRomNo9L - Medi', 13.00, 'NimbusRomNo9L'),
    ('ZTJCPR + NimbusRomNo9L - MediItal', 11.50, 'NimbusRomNo9L'),
    ('CHABPE + TimesNewRomanPSMT', 14.40, 'TimesNewRoman'),
    ('TimesNewRomanPS - ItalicMT', 13.30, 'TimesNewRoman'),
    ('LGAZPG + SegoeUI, Bold', 27.50, 'SegoeUI'),
    ('ALONFR + SegoeUI', 13.10, 'SegoeUI'),
    ('Helvetica - Bold', 16.70, 'Helvetica'),
    pytest.param(
        'Times - Roman',
        13.40,
        'Times',
        marks=pytest.mark.xfail(reason='TODO: solve roman problem'),
    ),
    ('CIDFont+F1', 6.60, 'F1'),
    ('Arial,Bold', 15.00, 'Arial'),
    ('ABCDEE + Verdana,Bold', 15.00, 'Verdana'),
    ('AIDZQU+Times-Roman', 13.00, 'Times'),
    ('KCXMNX+TeX-feymr10', 10.00, 'TeX'),
    ('JBLIUJ+Arial-BoldMT', 10.00, 'Arial'),
])
def test_font_convert_from_raw(font, scale, expected_name):
    parsed = rawmaker.fonts.parser.font_fromraw(font, scale)
    assert parsed

    assert '+' not in parsed.name, str(parsed)
    assert ',' not in parsed.name, str(parsed)

    assert parsed.name == expected_name, str(expected_name)


BOLD = iamraw.fonts.Weight.BOLD
MEDIUM = iamraw.fonts.Weight.MEDIUM
NORMAL = iamraw.fonts.Style.NORMAL
REGULAR = iamraw.fonts.Stretch.REGULAR


@pytest.mark.font
@pytest.mark.parametrize('font, expected, style', [
    ('ArialMT', 'Arial', None),
    ('TimesNewRomanPSMT', 'TimesNewRoman', None),
    ('TimesNewRomanPS-ItalicMT', 'TimesNewRoman', None),
    ('TimesNewRomanPS-BoldMT', 'TimesNewRoman', (BOLD, NORMAL, REGULAR)),
    ('DDPEIM+Helvetica-Bold', 'Helvetica', (BOLD, NORMAL, REGULAR)),
])
def test_font_name_fromraw(font, expected, style):
    parsed = rawmaker.fonts.parser.font_fromraw(font, scale=10.0)
    assert parsed.name == expected

    if not style:
        return
    assert parsed.weight == style[0]
    assert parsed.style == style[1]
    assert parsed.stretch == style[2]


@pytest.mark.parametrize('font, expected_name', [
    ('ADDAOP+AdvTT5ada87cc+fb4', 'AdvTT5ada87cc+fb4'),
])
def test_convert_font_from_raw_pdf_naming_problem(font, expected_name):
    parsed = rawmaker.fonts.parser.font_fromraw(font, scale=10.0)
    assert parsed
    assert parsed.name == expected_name, str(expected_name)


def test_strip_correct_bounding_box(td, mp):
    """This is an table like example. We have two columns. On the left side
    there is a shortcut column and on the right side there is the
    description of the shortcut. Two item must have a near y-coordinate
    because there are on the same line."""
    source = power.BACHELOR037_PDF
    config = rawmaker.parameter.ParsingConfiguration(line_margin=0.25)
    cmd = f'-i {source} --text --pages=1 {config.cmdline()}'
    tests.run(cmd, mp=mp)

    navigators = serializeraw.ptn_frompath(td.tmpdir)
    navigator = navigators[0]
    parsed = sorted(
        navigator,
        key=operator.attrgetter('bounding.y0', 'bounding.x0'),
    )
    bounding = {item.text.strip(): item.bounding for item in parsed}

    max_diff = 1.0
    mapping = [
        ('vs.', 'versus'),
        ('Abb.', 'Abbildung'),
    ]
    for first, second in mapping:
        assert utila.near(
            bounding[first].y1,
            bounding[second].y1,
            diff=max_diff,
        ), f'{first}: {bounding[first].y1} {second}: {bounding[second].y1}'


def test_strip_correct_bounding_box_master116(td, mp):
    source = power.MASTER116_PDF
    config = rawmaker.parameter.ParsingConfiguration(line_margin=0.25)
    cmd = f'-i {source} --text --pages=96 {config.cmdline()}'
    tests.run(cmd, mp=mp)

    navigators = serializeraw.ptn_frompath(td.tmpdir)
    navigator = navigators[0]
    parsed = sorted(
        navigator,
        key=operator.attrgetter('bounding.y0', 'bounding.x0'),
    )
    bounding = {item.text.strip(): item.bounding for item in parsed}

    max_diff = 5.0
    mapping = [
        ('BCU', 'Battery Control Unit'),
        ('eCVT', 'Electrical Continuously Variable Transmission'),
        ('EPA', 'United States Environmental Protection Agency'),
        ('GEN', 'Generator'),
        ('ICE', 'Internal Combustion Engine'),
        ('ISO', 'International Organization for Standardization'),
        ('SOC', 'State of Charge - relativer Ladezustand der Batterie'),
        ('Velodyn', 'Vehicle Longitudinal Dynamics'),
    ]
    for first, second in mapping:
        assert utila.near(
            bounding[first].y1,
            bounding[second].y1,
            diff=max_diff,
        ), f'{first}: {bounding[first].y1} {second}: {bounding[second].y1}'


def test_mining_fonts_bachelor37(td, mp):
    source = power.BACHELOR037_PDF
    tests.run(f'-i {source} --pages=5 --text --font', mp=mp)
    navigators = serializeraw.ptn_frompath(td.tmpdir)
    page5 = navigators[0]
    firstline = page5[1]
    assert firstline.style.content[0].size == 11.04
