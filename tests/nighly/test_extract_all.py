# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
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

import power
import pytest
import utila
import utilatest

import tests
import tests.linero_
import tests.pdfinfo_
import tests.resources


def pdf():
    located = glob.glob(f'{tests.resources.RESOURCES}/**/*.pdf', recursive=True)
    located.extend(power.PDF)
    result = []
    for item in located:
        if any((test in str(item) for test in SKIP)):
            continue
        result.append(item)
    return result


def convert_path(path: str, name_length_max: int = 35) -> str:
    """Convert to relative and forward slashed path, remove leading slash."""
    relative = utila.make_relative(path, power.REPOSITORY)
    result = relative.replace('\\', '_')[1:]
    result = result.replace('/', '_')
    result = result.replace('.', '_')
    result = result[-name_length_max:]
    return result


SKIP = {
    'PDF32000_2008.pdf',
    'diss406.pdf',
    'bachelor085.pdf',
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
        ) for item in (pdf() if utilatest.NIGHTLY else pdf()[0:10])
    ]
    return result


@utilatest.skip_longrun
@pytest.mark.usefixtures('testdir')
@pytest.mark.parametrize('source', sources())
def test_rawmaker_linero(source, monkeypatch):
    # use first 5 pages for normal testing and extract complete document
    # only in nighly tests.
    layout = '--char_margin 5.0 --boxes_flow 1.0 --line_margin 0.3'
    pages = '' if utilatest.NIGHTLY else '--page=0:5'
    cmd = f'-i {source} {layout} -j=8 {pages} -VVV'
    tests.run(cmd, monkeypatch=monkeypatch)

    tests.linero_.run('', monkeypatch=monkeypatch)


@utilatest.skip_nightly
@pytest.mark.usefixtures('testdir')
@pytest.mark.parametrize('source', sources())
def test_pdfinfo(source, monkeypatch):
    cmd = f'-i {source}'
    tests.pdfinfo_.run(cmd, monkeypatch=monkeypatch)


def test_locate_test_resources():
    located = pdf()
    assert len(located) > 20
