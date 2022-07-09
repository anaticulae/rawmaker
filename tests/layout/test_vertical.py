# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import texmex
import utilatest

import tests


@pytest.mark.parametrize('page, vertical, expected_empty', [
    (8, True, False),
    (8, False, False),
    (7, True, True),
])
@utilatest.longrun
def test_parse_docu009_vertically(
    page,
    vertical,
    expected_empty,
    td,
    mp,
):
    root = td.tmpdir
    source = power.ORDER009_PDF
    flag = '--detect_vertical' if vertical else ''
    config = '--char_margin=2.0 --word_margin=0.1 --line_margin=0.001'
    cmd = f'-i {source} --text --pages={page} {flag} {config}'
    tests.run(cmd, mp=mp)

    if vertical:
        mode = texmex.PageTextNavigatorMode.VERTICAL
    else:
        mode = texmex.PageTextNavigatorMode.HORIZONTAL

    loaded = serializeraw.ptn_frompath(root, mode=mode)[0]
    content = loaded[:]
    empty = [] == content
    assert empty == expected_empty, str(content)
