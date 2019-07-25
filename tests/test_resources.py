# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""This test suite must run all pdf-files located in kiwi-project especially
in `power` library.

Use multiprocessing to reduce test duration.
"""

from glob import glob
from os.path import join

from pytest import fixture
from pytest import mark
from pytest import param
from utila import SUCCESS
from utila import run

from tests import skip_virtual
from tests.resources import RESOURCES

COMMAND = 'power'


def prepare_resources():
    command = 'power --all -o %s' % RESOURCES

    completed = run(command, RESOURCES)
    assert completed.returncode == SUCCESS, str(completed)


def locate_all_pdfs():
    pattern = join(RESOURCES, '**/*.pdf')
    located = glob(pattern, recursive=True)
    return located


def test_locate_test_resources():
    located = locate_all_pdfs()
    assert located


@fixture(params=[
    param('--char_margin 100.0 --boxes_flow 1.0', id='toc'),
    param('--char_margin 5.0 --boxes_flow 1.0 --line_margin 0.3', id='default'),
])
def layout(request):
    return request.param


HUGE_RUN_PARAMETER = [
    param(
        item,
        id=item.replace(RESOURCES, ''),
    ) for item in locate_all_pdfs()
]


# TODO: Installing requirements via pip does not install the packages as wheel,
# therefore the project structure got lost. This is required, that power can
# access `repository` path.
@skip_virtual  # TODO: REMOVE AFTER FIXING PROBLEM WITH SETUP TOOLS
@mark.parametrize('pdffile', HUGE_RUN_PARAMETER)
@mark.slow
def test_run_huge(testdir, pdffile, layout):
    command = 'rawmaker -i %s %s' % (pdffile, layout)
    completed = run(command)
    assert completed.returncode == SUCCESS, str(completed)
