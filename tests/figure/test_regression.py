# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import utilatest

import tests


@utilatest.nightly
def test_extract_figures_memory_error(testdir, monkeypatch, capsys):
    # TODO: VALIDATE THIS UNIT TEST. THE MEMORY ERROR LOOKS QUITE
    # CONFUSING, PAY ATENTION TO THE PAGE NUMBERS
    source = power.BACHELOR085_PDF
    tests.run(f'-i {source}  --figures --pages=75:', monkeypatch=monkeypatch)
    stderr = capsys.readouterr().err
    assert 'could not render' in stderr, str(stderr)


def test_nofigure_diss266_pagex(testdir, monkeypatch):
    # TODO: INVESTIGATE WHERE DOE THESE RECTANGLES COME FROM!
    source = power.DISS266_PDF
    pages = '27,28,61'
    tests.run(f'-i {source} --figures --pages={pages}', monkeypatch=monkeypatch)
    # do not detect any figures on page 27, 28, 61
    assert not os.path.exists('rawmaker__figures_figures')
