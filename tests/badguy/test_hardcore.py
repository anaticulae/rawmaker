# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import utilotest

import tests


@utilotest.nightly
def test_book636(td, mp):
    pytest.skip('we require a weekly decorator')
    # TODO: CONVERT TO WEEKLY
    cmd = f'-i {hoverpower.HC_BOOK636} -o {td.tmpdir} -j1'
    tests.run(cmd, mp=mp)
