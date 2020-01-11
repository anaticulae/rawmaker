# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import os

import pytest
import utila

import pdfinfo
import pdfinfo.data
import pdfinfo.info
import pdfinfo.version
import tests.pdfinfo_
import tests.resources


@pytest.mark.parametrize('command', [
    '--help',
    pytest.param(f'-i {tests.resources.NO_PDF}', id='invalid_pdffile'),
    pytest.param(f'-i {tests.resources.TOC_PDF}', id='valid_restructured'),
])
def test_pdfinfo_run(command, testdir, monkeypatch):  #pylint: disable=W0613
    """Run help and version and format command to reach basic test coverage"""
    tests.pdfinfo_.run_success(command, monkeypatch=monkeypatch)


@pytest.mark.parametrize(
    'command',
    [
        pytest.param(f'-i {pdfinfo.ROOT}', id='input_directory'),
    ],
)
def test_pdfinfo_run_invalid(command, testdir, monkeypatch):  #pylint: disable=W0613
    """Run help and version and format command to reach basic test coverage"""
    tests.pdfinfo_.run_failure(command, monkeypatch=monkeypatch)


def test_pdfinfo_status_valid(testdir, monkeypatch):
    workspace = str(testdir)
    valid = pdfinfo.data.PdfInfo(
        pages=42,
        generator=pdfinfo.info.Generator.MSWord,
        version=pdfinfo.version.Version(1, 5),
    )
    raw = pdfinfo.data.jsonify(valid)
    path = os.path.join(workspace, 'pdfinfo.json')
    utila.file_create(path, raw)

    tests.pdfinfo_.run_success('--status', monkeypatch=monkeypatch)


def test_pdfinfo_status_invalid(testdir, monkeypatch):
    workspace = str(testdir)
    path = os.path.join(workspace, 'pdfinfo.json')
    utila.file_create(path, '{}')

    returncode = tests.pdfinfo_.run_failure('--status', monkeypatch=monkeypatch)
    assert returncode == pdfinfo.INVALID_PDF
