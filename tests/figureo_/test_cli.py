# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import pytest
import utila

import tests.figureo_
import tests.resources


@pytest.mark.parametrize('command', [
    '--help',
])
def test_figures_help(command, testdir, monkeypatch):  #pylint: disable=W0613
    """Run help and version and format command to reach basic test coverage"""
    tests.figureo_.run(command, monkeypatch=monkeypatch)


def test_figures_run_master116(testdir, monkeypatch):  #pylint: disable=W0613
    """Run help and version and format command to reach basic test coverage"""
    source = tests.resources.MASTER116
    outpath = os.path.join(testdir.tmpdir, 'output')
    cmd = f'-i {source} --pages=17:24 -o {outpath}'
    tests.figureo_.run(cmd, monkeypatch=monkeypatch)

    expected_file_count = 7 * 2
    written = utila.file_list(outpath)
    assert len(written) == expected_file_count, str(written)
