# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import utila

import tests.cleanup


def test_run_cleanup(monkeypatch):
    tests.cleanup.run('--help', monkeypatch=monkeypatch)


def test_cleanup_bachelor56(testdir, monkeypatch):
    source = power.link(power.BACHELOR056_PDF)
    utila.copy_content(
        source,
        testdir.tmpdir,
        pattern='(rawmaker__text|rawmaker__fonts)_*.yaml',
    )
    tests.cleanup.run(
        '-i . -o . --postfix=cleaned',
        monkeypatch=monkeypatch,
    )
    assert 0
