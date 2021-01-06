# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import power
import pytest
import serializeraw
import utilatest

import tests


def test_linero_figure_extract():
    pytest.skip('work in progress')
    source = power.link(power.BOOK007_PDF)
    pages = (5)
    lines = iamraw.path.line(source)
    textpositions = iamraw.path.textposition(source)

    lines = serializeraw.load_lines(lines, pages=pages)
    textpositions = serializeraw.load_textpositions(textpositions, pages=pages)

    lines = lines[0].content
    textpositions = textpositions[0].content

    # figures = linero.features.figure.analyse_page(lines, textpositions)
    # assert figures
    # assert 0


@utilatest.skip_nightly
def test_extract_figures_memory_error(testdir, monkeypatch, capsys):
    # TODO: VALIDATE THIS UNIT TEST. THE MEMORY ERROR LOOKS QUITE
    # CONFUSING, PAY ATENTION TO THE PAGE NUMBERS
    source = power.BACHELOR085_PDF
    tests.run(f'-i {source}  --figures --pages=75:', monkeypatch=monkeypatch)
    stderr = capsys.readouterr().err
    assert 'could not render' in stderr, str(stderr)
