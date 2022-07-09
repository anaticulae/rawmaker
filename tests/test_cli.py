#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import os

import power
import pytest
import utila
import utilatest

import tests
from tests import failure
from tests import run
from tests.resources import HELLO_WORLD


@pytest.mark.parametrize('command', [
    ['--help'],
    ['-i', HELLO_WORLD, '-o', 'output', '-j', '5'],
    ['-i', power.DOCU027_PDF, '-o', 'output'],
    ['-i', power.DOCU035_PDF, '-o', 'output'],
])
@pytest.mark.usefixtures('testdir')
@utilatest.nightly
def test_run_rawmaker(command, mp):
    """Run help and version and format command to reach basic test coverage"""
    run(command, mp=mp)


@pytest.mark.parametrize('command', [
    [],
    ['-i', '.', '-o', 'output'],
])
@pytest.mark.usefixtures('testdir')
def test_run_rawmaker_failed_empty_folder(command, mp):
    """Run help and version and format command to reach basic test coverage"""
    failure(command, mp=mp)


def test_run_rawmaker_empty_input(td, capsys, mp):
    """Run help and version and format command to reach basic test coverage"""
    td.mkdir('empty')
    command = ['-i', 'empty', '-o', 'output']  # no pdf input
    failure(command, mp=mp)
    stderr = utilatest.stderr(capsys)
    assert '[ERROR]' in stderr


@pytest.mark.parametrize(
    'command',
    [
        # DO NOT REMOVE A SINGLE SOURCE OF THIS TEST
        ['-i', power.DOCU009_PDF, '-o', 'output'],
    ])
@pytest.mark.usefixtures('testdir')
@utilatest.nightly
def test_run_rawmaker_for_regression(command, mp):
    """This test run the rawmaker with problematic resources which led to an
    error on parsing/converting the document in the past."""
    run(command, mp=mp)


@pytest.mark.parametrize('pages', [
    '5:10',
    '0',
])
@pytest.mark.usefixtures('testdir')
@utilatest.longrun
def test_run_rawmaker_with_pages(mp, pages):
    """Extract special pages"""
    cmd = ['-i', power.DOCU027_PDF, '-o', 'output', '--pages', pages, '-VVV']
    run(cmd, mp=mp)


def test_run_rawmaker_with_broken_resource(td, mp):
    """Create broken pdf resource, run reader and check that error is
    handled correctly."""
    root = td.tmpdir
    brokenpath = os.path.join(root, 'broken.pdf')
    utila.file_create(brokenpath, 'content = non valid pdf document')
    command = f'-i {root} --linter'
    failure(command, mp=mp)
    # check that result is written
    files_written = list(os.scandir(root))
    # broken file + developer.lin and user.lin
    expected = 3
    assert len(files_written) == expected, str(files_written)


@utilatest.longrun
def test_rawmaker_cli_run_file_without_extention(td, mp):
    source = os.path.join(td.tmpdir, 'hello')
    utila.file_copy(power.DOCU027_PDF, source)
    tests.run(f'-i {source}', mp=mp)


@pytest.mark.usefixtures('testdir')
@utilatest.nightly
def test_rawmaker_with_prefix(mp):
    """Regression test to ensure that horizontal step loads the correct
    lines when using prefix."""
    source = power.BACHELOR037_PDF
    cmd = f'-i {source} --pages=0:5 --prefix=oneline --line --horizontals'
    tests.run(cmd, mp=mp)
