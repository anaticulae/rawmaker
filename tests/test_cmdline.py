#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

from pytest import mark
from utila import run
from utila.test import skip_nonvirtual

from rawmaker import ROOT
from tests import run_failure
from tests import run_success
from tests.resources import DOCUMENTATION_TWINE
from tests.resources import DOCUMENTATION_TWINE_PDF
from tests.resources import EMPTY_PDF_FOLDER
from tests.resources import PORTING_PYTHON3
from tests.resources import RESTRUCTURED_PDF


@skip_nonvirtual
def test_install_and_run_rawmaker():
    install_and_run = 'python setup.py install && rawmaker --help'
    completed = run(install_and_run, cwd=ROOT)
    assert completed.returncode == 0, completed.stdout + completed.stderr


@mark.parametrize('command', [
    ['--help'],
    ['-i', DOCUMENTATION_TWINE, '-o', 'output'],
    ['-i', DOCUMENTATION_TWINE_PDF, '-o', 'output'],
    ['-i', RESTRUCTURED_PDF, '-o', 'output'],
])
def test_run_rawmaker(command, testdir, monkeypatch):  #pylint: disable=W0613
    """Run help and version and format command to reach basic test coverage"""
    run_success(command, monkeypatch=monkeypatch)


@mark.parametrize('command', [
    [],
    ['-i', EMPTY_PDF_FOLDER, '-o', 'output'],
])
def test_run_rawmaker_failed(command, testdir, monkeypatch):  #pylint: disable=W0613
    """Run help and version and format command to reach basic test coverage"""
    run_failure(command, monkeypatch=monkeypatch)


def test_run_rawmaker_empty_input(testdir, capsys, monkeypatch):  #pylint: disable=W0613
    """Run help and version and format command to reach basic test coverage"""
    testdir.mkdir('empty')
    command = ['-i', 'empty', '-o', 'output']  # no pdf input
    run_failure(command, monkeypatch=monkeypatch)

    stderr = capsys.readouterr().err
    assert '[ERROR]' in stderr


@mark.parametrize(
    'command',
    [
        # DO NOT REMOVE A SINGLE SOURCE OF THIS TEST
        ['-i', PORTING_PYTHON3, '-o', 'output'],
    ])
def test_run_rawmaker_for_regression(command, testdir, monkeypatch):  #pylint: disable=W0613
    """This test run the rawmaker with problematic resources which led to an
    error on parsing/converting the document in the past."""
    run_success(command, monkeypatch=monkeypatch)
