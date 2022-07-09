# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import utilatest

import tests


@utilatest.nightly
def test_book636(td, mp):
    cmd = f'-i {power.HC_BOOK636} -o {td.tmpdir} -j1'
    tests.run(cmd, mp=mp)
