# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import utila
import utilatest

import tests


@utilatest.longrun  # requires installed package
def test_rawmaker_cli_superfast(testdir, monkeypatch):
    source = power.DOCU27_PDF
    cmd = ['--sf', '-i', source, '--text']
    tests.run(cmd, monkeypatch=monkeypatch)


@utilatest.longrun  # requires installed package
def test_rawmaker_cli_superfast_compare(testdir, monkeypatch):
    """Ensure that --superfast produces the same results as without superfast"""
    source = power.DOCU27_PDF

    workspace = str(testdir)
    first = os.path.join(workspace, 'first')
    second = os.path.join(workspace, 'second')
    os.makedirs(first)
    os.makedirs(second)

    with utila.chdir(first):
        cmd = ['--sf', '-i', source, '--text']
        tests.run(cmd, monkeypatch=monkeypatch)

    with utila.chdir(second):
        cmd = ['-i', source, '--text']
        tests.run(cmd, monkeypatch=monkeypatch)

    ftext = utila.file_read(os.path.join(first, 'rawmaker__text_text.yaml'))
    stext = utila.file_read(os.path.join(second, 'rawmaker__text_text.yaml'))

    assert ftext == stext

    first_positions = utila.file_read(
        os.path.join(first, 'rawmaker__text_positions.yaml'))
    second_positions = utila.file_read(
        os.path.join(second, 'rawmaker__text_positions.yaml'))

    assert first_positions == second_positions
