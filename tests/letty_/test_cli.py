# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest

import tests.letty_
import tests.resources


@pytest.mark.parametrize('command', [
    '--help',
])
def test_letty_cli_run(command, testdir, monkeypatch):  #pylint: disable=W0613
    """Run help and version and format command to reach basic test coverage"""
    tests.letty_.run_success(command, monkeypatch=monkeypatch)


@pytest.mark.parametrize('command', [
    '',
])
def test_letty_cli_run_failure(command, testdir, monkeypatch):  #pylint: disable=W0613
    tests.letty_.run_failure(command, monkeypatch=monkeypatch)


def test_letty_whitespaces(monkeypatch, capsys):  #pylint: disable=W0613
    cmd = f'-i {power.link(power.DOCU13_PDF)} --whitespace'
    tests.letty_.run_success(cmd, monkeypatch=monkeypatch)

    stdout = capsys.readouterr().out

    number_of_whitespaces = int(stdout.strip())
    assert number_of_whitespaces > 300, stdout
