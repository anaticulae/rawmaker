# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import power
import serializeraw

import tests


def test_whitespace_extractor_bachelor56page49(testdir, monkeypatch):
    root = testdir.tmpdir
    source = power.BACHELOR056_PDF
    # oneline
    config = '--boxes_flow=1.0 --char_margin=100.0 --line_margin=0.0001'
    cmd = f'-i {source} --text --pages=49 --prefix=oneline {config}'
    tests.run(cmd, monkeypatch=monkeypatch)
    text = iamraw.path.text(root, prefix='oneline')
    text = serializeraw.load_document(text)[0]
    positions = iamraw.path.textposition(root, prefix='oneline')
    positions = serializeraw.load_textpositions(positions)[0].content.values()
    # select bounding
    positions = [item[0] for item in positions]

    expected = [
        (positions[15], text[15]),
        (positions[16], text[16]),
        (positions[18], text[18]),
    ]
    for pos, item in expected:
        assert pos[0] > 135.0, str(pos) + '   ' + item.text
