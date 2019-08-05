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
from utila import skip_longrun

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


def convert_path(path):
    """Convert to relative and forward slashed path, remove leading slash"""
    return path.replace(RESOURCES, '').replace('\\', '/')[1:]


# documents which does not pass the current implementation
UNSUPPORTED_DOCUMENTS = {
    'homework/page_40_images_toc.pdf',
    'paper/page_6_double_column.pdf',
    'paper/page_6_double_column_with_math.pdf',  # feymr10
}

HUGE_RUN_PARAMETER = [
    param(
        item,
        id=convert_path(item),
        marks=mark.xfail(reason="unsupported font format with current impl"),
    ) if convert_path(item) in UNSUPPORTED_DOCUMENTS else param(
        item,
        id=convert_path(item),
    ) for item in locate_all_pdfs()
]


# TODO: Installing requirements via pip does not install the packages as wheel,
# therefore the project structure got lost. This is required, that power can
# access `repository` path.
# @skip_virtual  # TODO: REMOVE AFTER FIXING PROBLEM WITH SETUP TOOLS
@mark.parametrize('pdffile', HUGE_RUN_PARAMETER)
@skip_longrun
def test_run_huge(testdir, pdffile, layout):  # pylint:disable=W0621
    command = 'rawmaker -i %s %s -p=4' % (pdffile, layout)
    completed = run(command)
    assert completed.returncode == SUCCESS, str(completed)
