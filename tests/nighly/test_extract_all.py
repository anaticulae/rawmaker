# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Nighly: Extract All PDF Files
=============================

This long running nightly test must ensure that all pdf files in
reposity are extractable by rawmaker and exit with exitcode 0.
"""

import glob

import pytest
import utila

import tests
import tests.figureo_
import tests.linero_
import tests.pdfinfo_
import tests.resources


def pdf():
    located = glob.glob(f'{tests.resources.RESOURCES}/**/*.pdf', recursive=True)
    result = []
    for item in located:
        if any((test in str(item) for test in SKIP)):
            continue
        result.append(item)
    return result


def convert_path(path: str) -> str:
    """Convert to relative and forward slashed path, remove leading slash."""
    relative = utila.make_relative(path, tests.resources.RESOURCES)
    result = relative.replace('\\', '_')[1:]
    return result


SKIP = {
    'PDF32000_2008.pdf',
}

# documents which does not pass the current implementation
# add location to mark document as unsupported
UNSUPPORTED_DOCUMENTS = {}


def sources():
    result = [
        pytest.param(
            item,
            id=convert_path(item),
            marks=pytest.mark.xfail(reason="unsupported implementation"),
        ) if convert_path(item) in UNSUPPORTED_DOCUMENTS else pytest.param(
            item,
            id=convert_path(item),
        ) for item in pdf()
    ]
    return result


@utila.skip_longrun
@pytest.mark.parametrize('source', sources())
def test_nightly_rawmaker_and_linero(source, testdir, monkeypatch):  # pylint:disable=W0621
    # use first 10 pages for normal testing and extract complete document
    # only in nighly tests.
    layout = '--char_margin 5.0 --boxes_flow 1.0 --line_margin 0.3'
    pages = '' if utila.NIGHTLY else '--page=0:5'
    cmd = f'-i {source} {layout} -j=8 {pages} -VVV'
    tests.run_success(cmd, monkeypatch=monkeypatch)

    tests.linero_.run_success('', monkeypatch=monkeypatch)


@utila.skip_nightly
@pytest.mark.parametrize('source', sources())
def test_nightly_pdfinfo(source, testdir, monkeypatch):  # pylint:disable=W0621
    cmd = f'-i {source}'
    tests.pdfinfo_.run_success(cmd, monkeypatch=monkeypatch)


@utila.skip_nightly
@pytest.mark.parametrize('source', sources())
def test_nightly_figureo(source, testdir, monkeypatch):  # pylint:disable=W0621
    cmd = f'-i {source}'
    tests.figureo_.run(cmd, monkeypatch=monkeypatch)


def test_locate_test_resources():
    located = pdf()
    assert len(located) > 20
