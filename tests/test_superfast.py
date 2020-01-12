# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import os

import utila

import tests
import tests.resources


def test_rawmaker_cli_superfast(testdir, monkeypatch):
    source = tests.resources.RESTRUCTURED_PDF
    cmd = ['--sf', '-i', source, '--text']
    tests.run_success(cmd, monkeypatch=monkeypatch)


def test_rawmaker_cli_superfast_compare(testdir, monkeypatch):
    """Ensure that --superfast produces the same results as without superfast"""
    source = tests.resources.RESTRUCTURED_PDF

    workspace = str(testdir)
    first = os.path.join(workspace, 'first')
    second = os.path.join(workspace, 'second')
    os.makedirs(first)
    os.makedirs(second)

    with utila.chdir(first):
        cmd = ['--sf', '-i', source, '--text']
        tests.run_success(cmd, monkeypatch=monkeypatch)

    with utila.chdir(second):
        cmd = ['-i', source, '--text']
        tests.run_success(cmd, monkeypatch=monkeypatch)

    first_text = utila.file_read(
        os.path.join(first, 'rawmaker__text_text.yaml'))
    second_text = utila.file_read(
        os.path.join(second, 'rawmaker__text_text.yaml'))

    assert first_text == second_text

    first_positions = utila.file_read(
        os.path.join(first, 'rawmaker__text_positions.yaml'))
    second_positions = utila.file_read(
        os.path.join(second, 'rawmaker__text_positions.yaml'))

    assert first_positions == second_positions
