# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""This test suite must run all pdf-files located in kiwi-project especially
in `power` library.

Use multiprocessing to reduce test duration.
"""

import glob
import os

import pytest
import utila

import tests.resources

COMMAND = 'power'


def prepare_resources():
    command = 'power --all -o %s' % tests.resources.RESOURCES

    completed = utila.run(command, tests.resources.RESOURCES)
    assert completed.returncode == utila.SUCCESS, str(completed)


def locate_all_pdfs():
    pattern = os.path.join(tests.resources.RESOURCES, '**/*.pdf')
    located = glob.glob(pattern, recursive=True)
    return located


def test_locate_test_resources():
    located = locate_all_pdfs()
    assert located


@pytest.fixture(params=[
    # TODO: do not run rawmaker twice to reduce required test power, activate
    # later.
    # param('--char_margin 100.0 --boxes_flow 1.0', id='toc'),
    pytest.param(
        '--char_margin 5.0 --boxes_flow 1.0 --line_margin 0.3',
        id='default',
    ),
])
def layout(request):
    return request.param


def convert_path(path):
    """Convert to relative and forward slashed path, remove leading slash"""
    return path.replace(tests.resources.RESOURCES, '').replace('\\', '/')[1:]


# documents which does not pass the current implementation
# add location to mark document as unsupported
UNSUPPORTED_DOCUMENTS = {}

HUGE_RUN_PARAMETER = [
    pytest.param(
        item,
        id=convert_path(item),
        marks=pytest.mark.xfail(
            reason="unsupported font format with current impl"),
    ) if convert_path(item) in UNSUPPORTED_DOCUMENTS else pytest.param(
        item,
        id=convert_path(item),
    ) for item in locate_all_pdfs()
]


# TODO: Installing requirements via pip does not install the packages as wheel,
# therefore the project structure got lost. This is required, that power can
# access `repository` path.
# @skip_virtual  # TODO: REMOVE AFTER FIXING PROBLEM WITH SETUP TOOLS
@pytest.mark.parametrize('pdffile', HUGE_RUN_PARAMETER)
@utila.skip_longrun
def test_run_huge(testdir, pdffile, layout):  # pylint:disable=W0621
    # use first 10 pages for normal testing and extract complete document
    # only in nighly tests.
    pages = '' if utila.NIGHTLY else '--page=0:10'
    cmd = f'rawmaker -i {pdffile} {layout} -j=4 {pages} -VVV'
    result = utila.run(cmd)

    assert result.returncode == utila.SUCCESS, utila.format_completed(result)
