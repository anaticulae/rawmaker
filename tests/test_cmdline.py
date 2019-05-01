#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

from pytest import mark
from utila import run
from utila.test import skip_nonvirtual

from rawmaker import ROOT
from tests import run_failure
from tests import run_success
from tests.resource import HELLO_WORLD


@skip_nonvirtual
def test_install_and_run_rawmaker(testdir):
    install_and_run = 'python setup.py install && rawmaker --help'
    completed = run(install_and_run)
    assert completed.returncode == 0, completed.stdout + completed.stderr


@mark.parametrize('command', [
    ['--help'],
    ['-i', HELLO_WORLD, '-o', 'output'],
])
def test_run_rawmaker(command, testdir, monkeypatch):  #pylint: disable=W0613
    """Run help and version and format command to reach basic test coverage"""
    run_success(command, monkeypatch)


@mark.parametrize('command', [
    [],
])
def test_run_rawmaker_failed(command, testdir, monkeypatch):  #pylint: disable=W0613
    """Run help and version and format command to reach basic test coverage"""
    run_failure(command, monkeypatch)
