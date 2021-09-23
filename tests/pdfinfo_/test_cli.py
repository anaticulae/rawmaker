# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import iamraw
import power
import pytest
import serializeraw
import utila
import utilatest

import pdfinfo
import pdfinfo.info
import pdfinfo.version
import tests.pdfinfo_
import tests.resources


@pytest.mark.parametrize('command', [
    '--help',
    pytest.param(f'-i {tests.resources.NO_PDF}', id='invalid_pdf'),
    pytest.param(f'-i {tests.resources.NO_PDF} --format=yaml', id='use yaml'),
    pytest.param(f'-i {power.DOCU027_PDF}', id='valid_pdf'),
    pytest.param(f'-i {power.MASTER116_PDF}', id='master116'),
    pytest.param(f'-i {power.MASTER089_PDF}', id='master89'),
    pytest.param(f'-i {power.MASTER098_PDF}', id='master98'),
])
def test_pdfinfo_run(command, testdir, monkeypatch):  #pylint: disable=W0613
    tests.pdfinfo_.run(command, monkeypatch=monkeypatch)


@pytest.mark.parametrize(
    'command',
    [
        pytest.param(f'-i {pdfinfo.ROOT}', id='input_directory'),
        pytest.param(f'-i {__file__} --strict', id='no_pdf_file'),
    ],
)
def test_pdfinfo_run_invalid(command, testdir, monkeypatch):  #pylint: disable=W0613
    tests.pdfinfo_.failure(command, monkeypatch=monkeypatch)


def test_pdfinfo_status_valid(testdir, monkeypatch):
    workspace = str(testdir)
    valid = iamraw.PDFInfo(
        pages=42,
        generator=iamraw.Generator.MSWORD,
        version=iamraw.PDFVersion(1, 5),
    )
    raw = serializeraw.dump_pdfinfo(valid)
    path = os.path.join(workspace, 'pdfinfo.json')
    utila.file_create(path, raw)

    tests.pdfinfo_.run('--status', monkeypatch=monkeypatch)


def test_pdfinfo_status_invalid(testdir, monkeypatch):
    workspace = str(testdir)
    path = os.path.join(workspace, 'pdfinfo.json')
    utila.file_create(path, '{}')

    returncode = tests.pdfinfo_.failure('--status', monkeypatch=monkeypatch)
    assert returncode == pdfinfo.INVALID_PDF


def test_pdfinfo_stdout(testdir, monkeypatch, capsys):
    root = testdir.tmpdir
    source = power.DOCU027_PDF
    with utilatest.increased_filecount(root, mindiff=0, maxdiff=0):
        tests.pdfinfo_.run(f'-i {source}', monkeypatch=monkeypatch)
    stdout = utilatest.stdout(capsys)
    expected = (
        '{"pages": 27, "generator": "latex", "version": {"major": 1, '
        '"minor": 5}, "meta": {"author": "", "title": "", "subject": "",')
    assert expected in stdout  # do not verify all parsed meta data
