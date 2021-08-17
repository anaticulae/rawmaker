# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw

import rawmaker.features
import rawmaker.parameter
import tests


def test_toc_parametrization():
    """Test parametrization to get good result when parsing table of content

    This test is more for finding a good parameter, than for really testing.
    TODO: Improve this later. Don't know how to, yet.
    """
    with rawmaker.reader.read(power.DOCU027_PDF) as pdf:
        # Diff between chars which build a word
        config = rawmaker.parameter.ParsingConfiguration(char_margin=10.0)
        document = rawmaker.features.extract_content(pdf, config=config)
    page_with_toc = document[2]
    assert page_with_toc


# taken from genex
ONELINE = ('--prefix=oneline '
           '--text '
           '--boxes_flow=1.0 --char_margin=100.0 --line_margin=0.0001')


def test_regression_oneline_master078_toc(testdir, monkeypatch):
    """Do not skip chars which are detected as duplicated but the
    checker was not specific enough."""
    cmd = f'-i {power.MASTER078_PDF} --pages=2 ' + ONELINE
    tests.run(cmd, monkeypatch=monkeypatch)

    loaded = serializeraw.ptn_frompath(
        testdir.tmpdir,
        prefix='oneline',
    )[0]
    # the 4 was skipped in 2.2.1. because the state of 2.2 marked it as
    # done already.
    expected = [
        '2.2 Bussysteme der Gebäudeautomation . . . . . . . . . . . . . . 4',
        '2.2.1 Der Europäische Installationsbus (EIB) . . . . . . . . . 4'
    ]
    current = [str(line).strip() for line in loaded]
    assert all(item in current for item in expected)
