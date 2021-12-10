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

import tests


def test_text_rotated_master116page103(testdir, monkeypatch):
    cmd = f'-i {power.MASTER116_PDF} --text --pages=103'
    tests.run(cmd, monkeypatch=monkeypatch)
    loaded = serializeraw.load_document(testdir.tmpdir)[0]
    assert loaded
    assert len(loaded) == 3
