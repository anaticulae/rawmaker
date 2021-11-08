# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw

import tests


def test_fontrise_bachelor90page3(testdir, monkeypatch):
    """See: text.fix_fontrise"""
    source = power.BACHELOR090_PDF
    tests.run(f'-i {source} --pages=3 --text', monkeypatch=monkeypatch)

    loaded = serializeraw.ptn_frompath(testdir.tmpdir)[0]
    riseline = loaded[1]
    assert len(riseline.style.content) == 1
    style = riseline.style.content[0]
    assert style.rise == 0.0  # pylint:disable=C2001


def test_regression_font_rise_bachelor75page16(testdir, monkeypatch):
    """Obviously, this page does not contain any valid font rise."""
    cmd = f'-i {power.BACHELOR075_PDF} -o {testdir.tmpdir} --text --pages=16'
    tests.run(cmd, monkeypatch=monkeypatch)
    ptn = serializeraw.create_pagetextnavigators_frompath(testdir.tmpdir)[0]
    norise, rises = 0, 0
    for item in ptn:
        for style in item.style:
            width = style.end - style.start
            if style.rise:
                rises += width
            else:
                norise += width
    assert norise == 2161
    assert not rises


def test_regression_font_rise_bachelor75page1718(testdir, monkeypatch):
    cmd = f'-i {power.BACHELOR075_PDF} -o {testdir.tmpdir} --text --pages=17,18'
    tests.run(cmd, monkeypatch=monkeypatch)
    ptn = serializeraw.create_pagetextnavigators_frompath(testdir.tmpdir)[0]
    norise, rises = 0, 0
    for item in ptn:
        for style in item.style:
            width = style.end - style.start
            if style.rise:
                rises += width
            else:
                norise += width
    assert norise == 2145
    assert not rises
