# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utilatest

import tests.letty_


@pytest.mark.parametrize('command', [
    '--help',
])
def test_letty_cli_run(command, td, mp):  #pylint: disable=W0613
    """Run help and version and format command to reach basic test coverage"""
    tests.letty_.run(command, mp=mp)


@pytest.mark.parametrize('command', [
    '',
])
def test_letty_cli_failure(command, td, mp):  #pylint: disable=W0613
    tests.letty_.failure(command, mp=mp)


@utilatest.requires(power.DOCU013_PDF)
def test_letty_whitespaces(mp, capsys):  #pylint: disable=W0613
    cmd = f'-i {power.link(power.DOCU013_PDF)} --whitespace'
    tests.letty_.run(cmd, mp=mp)

    stdout = utilatest.stdout(capsys)
    number_of_whitespaces = int(stdout.strip())
    assert number_of_whitespaces > 300, stdout
