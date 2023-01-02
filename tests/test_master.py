# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utila
import utilatest

import tests
import tests.resources


@tests.ghost
@utilatest.longrun
def test_master_compare_vim(td, mp):
    """Update test data with `cmd` below. Copy from generated test."""
    if not utila.hasprog('diff'):
        pytest.skip(reason='require `diff` tool')
    cmd = f'-i {power.DOCU013_PDF} --images! --figures! -j8 --pages=1:4'
    tests.run(cmd, mp=mp)

    golden = tests.resources.GOLDEN_VIM
    current = td.tmpdir
    diff = f'diff -rd --suppress-common-lines -y {golden} {current}'

    completed = utila.run(diff)
    utila.error(completed.stdout)
    assert completed.returncode == utila.SUCCESS
