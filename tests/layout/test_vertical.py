# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import serializeraw

import tests.resources


def test_parse_howtoread_vertically(testdir, monkeypatch):
    root = testdir.tmpdir
    source = tests.resources.HOWTOREAD_PDF
    config = '--char_margin=2.0 --word_margin=0.1 --line_margin=0.001'
    cmd = f'-i {source} --text --pages=8 --detect_vertical {config}'
    tests.run_success(cmd, monkeypatch=monkeypatch)
    text = iamraw.path.text(root)
    text = serializeraw.load_document(text)[0]
    positions = iamraw.path.textposition(root)
    positions = serializeraw.load_textpositions(positions)[0].content.values()
    positions = list(positions)

    print()
    print()
    print()
    for pos, item in zip(positions, text):
        print(item.text)
        print(pos)
