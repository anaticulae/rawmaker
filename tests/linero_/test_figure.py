# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import serializeraw

import linero.features.figure
import rawmaker.path
import tests.resources


def test_linero_figure_extract():
    pytest.skip('work in progress')
    source = tests.resources.LEFTRIGHT_GENERATED
    pages = (5)
    lines = rawmaker.path.line(source)
    textpositions = rawmaker.path.textposition(source)

    lines = serializeraw.load_lines(lines, pages=pages)
    textpositions = serializeraw.load_textpositions(textpositions, pages=pages)

    lines = lines[0].content
    textpositions = textpositions[0].content

    figures = linero.features.figure.analyse_page(lines, textpositions)
    assert figures
    assert 0
