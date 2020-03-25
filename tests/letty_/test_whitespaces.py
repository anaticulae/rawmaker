# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import letty.quality.whitespace
import tests
import tests.resources


def test_whitespaces_count(testdir, monkeypatch):
    root = testdir.tmpdir
    path = tests.resources.MASTER72
    pages = (3, 4, 5)
    pages_raw = ','.join([str(item) for item in pages])
    cmd = f'-i {path} --pages={pages_raw} --text'
    tests.run_success(cmd, monkeypatch=monkeypatch)
    determined = letty.quality.whitespace.determine(root, pages)
    assert determined
    # more than hundret double white spaces
    assert determined[0].content[0][1] > 100, determined
