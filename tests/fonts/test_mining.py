# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import operator

import iamraw
import iamraw.path
import pytest
import serializeraw
import utila
import yaml

import rawmaker
import rawmaker.features
import rawmaker.features.fonts
import rawmaker.fonts.parser
import rawmaker.reader
import tests.resources


@utila.skip_longrun
def test_mining_fonts(testdir):
    header, content = rawmaker.features.fonts.work(tests.resources.TWINE_PDF)

    assert len(header) > 100
    assert len(content) > 300

    utila.file_create('header.yaml', header)
    utila.file_create('content.yaml', content)


def test_mining_fonts_cporting(testdir):
    header, content = rawmaker.features.fonts.work(
        tests.resources.HOW_TO_CPORTING_PDF)
    # XXX: Define good numbers
    assert len(header) > 100
    assert len(content) > 200


def test_minining_fonts_cporting_first_page():
    """Mine the first font of the document at the first page"""
    # TODO: Test mining last font of document
    with rawmaker.reader.read(tests.resources.HOW_TO_CPORTING_PDF) as pdf:
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


def test_mining_increasing_fonts():
    """The example contains the same sentences in fontsizes(8pt - 20pt)"""
    result = rawmaker.features.fonts.work(tests.resources.INCREASING_FONT_A4)
    header, _ = result

    font_sizes = [
        item['font']['scale']
        for item in yaml.load(header, Loader=yaml.FullLoader)
    ]
    font_sizes = font_sizes[0:-1]  # remove the last one(page number)

    increases = [
        first < second
        for (first, second) in zip(font_sizes[0:-1], font_sizes[1:])
    ]
    assert all(increases), str(font_sizes)

    expected_fontsizes = list(range(8, 21))
    font_sizes = utila.roundme(font_sizes, digits=0)
    assert font_sizes == expected_fontsizes


@pytest.fixture
def restructed_fonts():
    result = rawmaker.features.fonts.work(tests.resources.RESTRUCTURED_PDF)
    header = serializeraw.load_font_header(result[0])
    content = serializeraw.load_font_content(result[1])
    return header, content


def test_mining_fonts_restruct_page_5(restructed_fonts):  # pylint:disable=W0621
    """Mine the fifths page, compare only `Weight` for not beeing to
    specific"""
    header, content = restructed_fonts
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
    ('KCXMNX+TeX-feymr10', 10.00, 'TeX'),
    ('JBLIUJ+Arial-BoldMT', 10.00, 'Arial'),
])
def test_convert_font_from_raw(font, scale, expected_name):
    parsed = rawmaker.fonts.parser.font_fromraw(font, scale)
    assert parsed

    assert '+' not in parsed.name, str(parsed)
    assert ',' not in parsed.name, str(parsed)

    assert expected_name == parsed.name, str(expected_name)


@pytest.mark.parametrize('font, expected_name', [
    ('ADDAOP+AdvTT5ada87cc+fb4', 'AdvTT5ada87cc+fb4'),
])
def test_convert_font_from_raw_pdf_naming_problem(font, expected_name):
    parsed = rawmaker.fonts.parser.font_fromraw(font, scale=10.0)
    assert parsed

    assert expected_name == parsed.name, str(expected_name)


def test_strip_correct_bounding_box(testdir, monkeypatch):
    """This is an table like example. We have two columns. On the left side
    there is a shortcut column and on the right side there is the
    description of the shortcut. Two item must have a near y-coordinate
    because there are on the same line."""
    source = tests.resources.BACHELOR37
    config = rawmaker.parameter.ParsingConfiguration(line_margin=0.25)
    cmd = f'-i {source} --text --pages=1 {config.cmdline()}'
    tests.run_success(cmd, monkeypatch=monkeypatch)

    navigators = serializeraw.create_pagetextnavigators_frompath(testdir.tmpdir)
    navigator = navigators[0]
    parsed = sorted(
        [item for item in navigator],
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


def test_strip_correct_bounding_box_master116(testdir, monkeypatch):
    source = tests.resources.MASTER116
    config = rawmaker.parameter.ParsingConfiguration(line_margin=0.25)
    cmd = f'-i {source} --text --pages=96 {config.cmdline()}'
    tests.run_success(cmd, monkeypatch=monkeypatch)

    navigators = serializeraw.create_pagetextnavigators_frompath(testdir.tmpdir)
    navigator = navigators[0]
    parsed = sorted(
        [item for item in navigator],
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
