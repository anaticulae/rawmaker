# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utilo
import utilotest

import tests.rawmaker_automate_
import tests.resources


@utilotest.nightly
def test_cli_automate(td, mp):
    source = os.path.join(tests.resources.RESOURCES, 'increasing_fonts')
    cmd = f'-i {source} -o {td.tmpdir} -n3'
    assert os.path.exists(source)
    tests.rawmaker_automate_.run(cmd, mp=mp)
    assert len(utilo.directory_list(td.tmpdir)) == 3
