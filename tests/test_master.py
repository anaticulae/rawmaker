# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import tests
import tests.resources


@utila.skip_longrun
def test_master_compare_vim(testdir, monkeypatch):
    """Update test data with `cmd` below. Copy from generated test."""
    cmd = f'-i {tests.resources.VIM_PDF} -j8 --pages=1:4'
    tests.run_success(cmd, monkeypatch=monkeypatch)

    golden = tests.resources.GOLDEN_VIM
    current = testdir.tmpdir
    diff = f'diff -rd --suppress-common-lines -y {golden} {current}'

    completed = utila.run(diff)
    utila.error(completed.stdout)
    assert completed.returncode == utila.SUCCESS
