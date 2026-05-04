# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import serializeraw
import utilotest

import tests


def test_fontrise_bachelor90p3(td, mp):
    """See: text.fix_fontrise"""
    source = hoverpower.BACHELOR090_PDF
    tests.run(f'-i {source} --pages=3 --text', mp=mp)

    loaded = serializeraw.ptn_frompath(td.tmpdir)[0]
    riseline = loaded[1]
    assert len(riseline.style.content) == 1
    style = riseline.style.content[0]
    assert style.rise == 0.0  # pylint:disable=C2001


def test_regression_font_rise_bachelor75p16(td, mp):
    """Obviously, this page does not contain any valid font rise."""
    cmd = f'-i {hoverpower.BACHELOR075_PDF} -o {td.tmpdir} --text --pages=16'
    tests.run(cmd, mp=mp)
    ptn = serializeraw.ptn_frompath(td.tmpdir)[0]
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


@utilotest.longrun
def test_regression_font_rise_bachelor75p1718(td, mp):
    cmd = f'-i {hoverpower.BACHELOR075_PDF} -o {td.tmpdir} --text --pages=17,18'
    tests.run(cmd, mp=mp)
    ptn = serializeraw.ptn_frompath(td.tmpdir)[0]
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


def test_regression_diss273p38_footer_rise(td, mp):
    cmd = f'-i {hoverpower.DISS273_PDF} -o {td.tmpdir} --text --pages=38'
    tests.run(cmd, mp=mp)
    ptn = serializeraw.ptn_frompath(td.tmpdir)[0]
    line = ptn[36]
    expected = '[75]  Für Übersichtsartikel zur kupferkatalysierten'
    assert line.text.startswith(expected)
    assert line.style.content[0].rise


def test_regression_master72page14_footer_rise(td, mp):
    cmd = f'-i {hoverpower.MASTER072_PDF} -o {td.tmpdir} --text --pages=14'
    tests.run(cmd, mp=mp)
    ptn = serializeraw.ptn_frompath(td.tmpdir)[0]
    line = ptn[30]
    expected = '35 ebd.'
    assert line.text.startswith(expected)
    assert line.style.content[0].rise


def test_regression_hcdiss171p134(td, mp):
    cmd = f'-i {hoverpower.HC_DISS171} -o {td.tmpdir} --text --pages=134'
    tests.run(cmd, mp=mp)
    ptn = serializeraw.ptn_frompath(td.tmpdir)[0]
    line = ptn[61]
    expected = '2Notation:'
    assert line.text.startswith(expected)
    assert line.style.content[0].rise


def test_regression_master127p20(td, mp):
    cmd = f'-i {hoverpower.MASTER127_PDF} -o {td.tmpdir} --text --pages=20'
    tests.run(cmd, mp=mp)
    ptn = serializeraw.ptn_frompath(td.tmpdir)[0]
    line = ptn[-2]
    expected = '19 Fendt (2004)'
    assert line.text.startswith(expected)
    assert line.style.content[0].rise
