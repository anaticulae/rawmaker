# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import serializeraw
import utilo

import tests


def test_layout_fine_master72page3_horizontal_problem(td, mp):
    """Ensure that horizontal line is parsed before first footer text line.

    There was a problem, cause the position of the first line was
    parsed with a too low y0 coordinate.
    """
    source = td.tmpdir
    cmd = (f'-i {hoverpower.MASTER072_PDF} --text --line '
           '--horizontals --annotation --pages=3')
    tests.run(cmd, mp=mp)
    navigators = serializeraw.ptn_frompath(source)
    horizontal = serializeraw.load_horizontals(source)[0].content[0]
    firstpage = navigators[0]
    first_footer_line = firstpage[32]
    text = utilo.normalize_whitespaces(first_footer_line.text)
    assert text.startswith('1 Aus Gründen'), text
    msg = f'{first_footer_line} {horizontal}'
    assert first_footer_line.bounding.y0 > horizontal.box.y1, msg


@pytest.mark.xfail(reason='improve layout extraction')
def test_layout_fine_bachelor111page9_horizontal_problem(td, mp):
    source = td.tmpdir
    cmd = f'-i {hoverpower.BACHELOR111_PDF} --text --boxes --pages=9'
    tests.run(cmd, mp=mp)
    navigators = serializeraw.ptn_frompath(source)
    horizontal = serializeraw.load_horizontals(source)[0][0][-1]
    first_footer_line = navigators[0][34]
    text = utilo.normalize_whitespaces(first_footer_line.text)
    assert text.startswith('1Personal Digital'), text
    msg = f'{first_footer_line} {horizontal}'
    assert first_footer_line.bounding.y0 > horizontal.box.y1, msg
