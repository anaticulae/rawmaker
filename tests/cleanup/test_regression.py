# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import utilatest

import tests.cleanup.utils


@utilatest.longrun
def test_translate_diss143page25(testdir, monkeypatch):
    """Regression test to ensure that all lines are matched together.

    LEFT:           RIGHT
    1. A             1. A
       B             2. B
       C             3. C
    2. DEF           4. D
    3. GHF           5. E

    Before changing to single line, it was not possible to determine
    transformation: 2. B -> 1. B
    """
    source = power.DISS143_PDF
    tests.cleanup.utils.prepare(source, '25', testdir, monkeypatch)
    # fails before
    tests.cleanup.run('', monkeypatch=monkeypatch)
