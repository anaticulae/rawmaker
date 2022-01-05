# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utila
import utilatest

import tests.rawmaker_automate_
import tests.resources


@utilatest.nightly
def test_cli_automate(testdir, monkeypatch):
    source = os.path.join(tests.resources.RESOURCES, 'increasing_fonts')
    cmd = f'-i {source} -o {testdir.tmpdir} -n3'
    assert os.path.exists(source)
    tests.rawmaker_automate_.run(cmd, monkeypatch=monkeypatch)
    assert len(utila.directory_list(testdir.tmpdir)) == 3
