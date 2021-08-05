# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utila

import tests


def test_layout_fine_master72_page3_horizontal_problem(testdir, monkeypatch):
    """Ensure that horizontal line is parsed before first footer text
    line. There was a problem, cause the position of the first line was
    parsed with a to low y0 coordinate."""
    source = testdir.tmpdir
    cmd = (f'-i {power.MASTER072_PDF} --text --line '
           '--horizontals --annotation --pages=3')
    tests.run(cmd, monkeypatch=monkeypatch)

    navigators = serializeraw.create_pagetextnavigators_frompath(source)
    horizontal = serializeraw.load_horizontals(source)[0][0][0]
    firstpage = navigators[0]
    first_footer_line = firstpage[32]
    text = utila.normalize_whitespaces(first_footer_line.text)
    assert text.startswith('1 Aus Gründen'), text
    msg = f'{first_footer_line} {horizontal}'
    assert first_footer_line.bounding.y0 > horizontal.box.y1, msg


@pytest.mark.xfail(reason='improve layout extraction')
def test_layout_fine_bachelor111_page9_horizontal_problem(testdir, monkeypatch):
    source = testdir.tmpdir
    cmd = f'-i {power.BACHELOR111_PDF} --text --boxes --pages=9'
    tests.run(cmd, monkeypatch=monkeypatch)
    navigators = serializeraw.create_pagetextnavigators_frompath(source)
    horizontal = serializeraw.load_horizontals(source)[0][0][-1]
    first_footer_line = navigators[0][34]
    text = utila.normalize_whitespaces(first_footer_line.text)
    assert text.startswith('1Personal Digital'), text
    msg = f'{first_footer_line} {horizontal}'
    assert first_footer_line.bounding.y0 > horizontal.box.y1, msg
