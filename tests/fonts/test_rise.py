# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utilatest

import tests


def test_fontrise_bachelor90p3(testdir, monkeypatch):
    """See: text.fix_fontrise"""
    source = power.BACHELOR090_PDF
    tests.run(f'-i {source} --pages=3 --text', monkeypatch=monkeypatch)

    loaded = serializeraw.ptn_frompath(testdir.tmpdir)[0]
    riseline = loaded[1]
    assert len(riseline.style.content) == 1
    style = riseline.style.content[0]
    assert style.rise == 0.0  # pylint:disable=C2001


def test_regression_font_rise_bachelor75p16(testdir, monkeypatch):
    """Obviously, this page does not contain any valid font rise."""
    cmd = f'-i {power.BACHELOR075_PDF} -o {testdir.tmpdir} --text --pages=16'
    tests.run(cmd, monkeypatch=monkeypatch)
    ptn = serializeraw.ptn_frompath(testdir.tmpdir)[0]
    norise, rises = 0, 0
    for item in ptn:
        for style in item.style:
            width = style.end - style.start
            if style.rise:
                rises += width
            else:
                norise += width
    assert norise == 2132
    assert not rises


@utilatest.longrun
def test_regression_font_rise_bachelor75p1718(testdir, monkeypatch):
    cmd = f'-i {power.BACHELOR075_PDF} -o {testdir.tmpdir} --text --pages=17,18'
    tests.run(cmd, monkeypatch=monkeypatch)
    ptn = serializeraw.ptn_frompath(testdir.tmpdir)[0]
    norise, rises = 0, 0
    for item in ptn:
        for style in item.style:
            width = style.end - style.start
            if style.rise:
                rises += width
            else:
                norise += width
    assert norise == 2108
    assert not rises


def test_regression_diss273p38_footer_rise(testdir, monkeypatch):
    cmd = f'-i {power.DISS273_PDF} -o {testdir.tmpdir} --text --pages=38'
    tests.run(cmd, monkeypatch=monkeypatch)
    ptn = serializeraw.ptn_frompath(testdir.tmpdir)[0]
    line = ptn[36]
    expected = '[75]  Für Übersichtsartikel zur kupferkatalysierten'
    assert line.text.startswith(expected)
    assert line.style.content[0].rise
