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
import os

import pytest
import utila

import tests
import tests.figureo_
import tests.linero_
import tests.pdfinfo_
import tests.resources


def sources():
    root = tests.resources.RESOURCES
    with utila.chdir(root):
        collected = glob.glob('**/*.pdf')
    joined = [utila.make_absolute(item, cwd=root) for item in collected]
    result = [
        pytest.param(
            item,
            id=utila.make_relative(item, root=root),
        ) for item in joined
    ]
    return result


@utila.skip_nightly
@pytest.mark.parametrize('source', sources())
def test_nightly_extract_all_rawmaker_linero(source, testdir, monkeypatch):  # pylint:disable=W0621
    """Collect all existing pdf files an extract all features out of it."""
    source = os.path.join(tests.resources.RESOURCES, source)

    cmd = f'-i {source} -j=8'
    tests.run_success(cmd, monkeypatch=monkeypatch)

    cmd = '-j=8'
    tests.linero_.run_success(cmd, monkeypatch=monkeypatch)


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
