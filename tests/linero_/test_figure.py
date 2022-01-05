# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import power
import pytest
import serializeraw
import utilatest


@utilatest.requires(power.BOOK007_PDF)
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
