# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw

import rawmaker
import tests


def test_text_master110_bounding_x0_x1(testdir, monkeypatch):
    """There was the case that merging two chars/lines results in
    malformed bounding box. Skip merging bounding boxes solves this
    issue."""
    # layout is required to invoke error
    layout = '--char_margin=3.1 --boxes_flow=1.0 --line_margin=0.25'
    cmd = f'-i {power.MASTER110_PDF} --text --pages=60 {layout}'
    tests.run(cmd, monkeypatch=monkeypatch)
    loaded = serializeraw.load_textpositions(testdir.tmpdir)
    assert loaded


def test_negative_text_bounding_diss274page0(testdir, monkeypatch):
    # layout is required to invoke error
    layout = '--char_margin=3.1 --boxes_flow=1.0 --line_margin=0.25'
    cmd = f'-i {power.DISS274_PDF} --text --pages=0 {layout}'
    tests.run(cmd, monkeypatch=monkeypatch)
    navigators = serializeraw.ptn_frompath(testdir.tmpdir)
    navigator = navigators[0]
    # TODO: CHANGES AFTER INVESTIGATING PROBLEM WITH NEGATIVE TEXT CONTENT
    # ON LEFT BORDER.
    assert len(navigator) == 10


def test_text_bachelor67page63(testdir, monkeypatch):
    # layout is required to invoke error
    config = rawmaker.LAYOUT
    cmd = f'-i {power.BACHELOR067_PDF} --text --pages=63 {config}'
    tests.run(cmd, monkeypatch=monkeypatch)
    navigators = serializeraw.ptn_frompath(testdir.tmpdir)[0]
    text = [item.text.strip() for item in navigators]
    assert text[1] == '[AM14]'
    assert text[13] == '[Arm+15]'
