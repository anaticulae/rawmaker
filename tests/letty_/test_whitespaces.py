# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import utilotest

import letty.quality.whitespace
import tests


@utilotest.longrun
def test_whitespaces_count(td, mp):
    root = td.tmpdir
    path = hoverpower.MASTER072_PDF
    pages = (3, 4, 5)
    pages_raw = ','.join([str(item) for item in pages])
    cmd = f'-i {path} --pages={pages_raw} --text'
    tests.run(cmd, mp=mp)
    determined = letty.quality.whitespace.determine(root, pages)
    assert determined
    # more than hundred double white spaces
    assert determined > 100, determined
