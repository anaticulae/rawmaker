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


def test_fontrise_bachelor90_page3(testdir, monkeypatch):
    """See: text.fix_fontrise"""
    source = power.BACHELOR090_PDF
    tests.run(f'-i {source} --pages=3 --text', monkeypatch=monkeypatch)

    loaded = serializeraw.ptn_frompath(testdir.tmpdir)[0]
    riseline = loaded[1]
    assert len(riseline.style.content) == 1
    style = riseline.style.content[0]
    assert style.rise == 0.0
