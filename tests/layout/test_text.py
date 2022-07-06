# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import pytest
import serializeraw
import utila
import utilatest

import tests


def test_bachelor63_text_extraction(testdir, monkeypatch):
    """This is a regression test, which ensure that a `pdfminer` bug
    does no occurs again. There was a problem that some text was parsed
    twice and more."""
    root = testdir.tmpdir
    source = power.BACHELOR063_PDF
    config = ''
    cmd = f'-i {source} --text --pages=0 {config}'
    tests.run(cmd, monkeypatch=monkeypatch)

    navigator = serializeraw.ptn_frompath(root)[0]
    text = [str(item).strip() for item in navigator]
    unique = utila.make_unique(text)
    assert len(unique) == len(text), str(text)


def test_bachelor37_text_extraction_position_page4(testdir, monkeypatch):
    """Ensure that first and second line are splitted correctly. Before
    this test/patch there where merged together, but this is not the
    correct behavior.
    """
    root = testdir.tmpdir
    source = power.BACHELOR037_PDF
    cmd = f'-i {source} --text --pages=4'
    tests.run(cmd, monkeypatch=monkeypatch)

    navigator = serializeraw.ptn_frompath(root)[0]

    first = navigator[0].bounding
    second = navigator[1].bounding

    assert utila.near(70.92, first.x0), first.x0
    assert utila.near(371.04, second.x0), second.x0


@utilatest.longrun
def test_diss264_text_extraction_position_page17(testdir, monkeypatch, capsys):
    """Log non correct char conversion as an error."""
    # TODO: CHECK THIS TEST AFTER UPGRADING PDFMINER
    source = power.DISS264_PDF
    cmd = f'-i {source} --text --fonts --pages=17 -VVV'
    tests.run(cmd, monkeypatch=monkeypatch)
    stdout = utilatest.stderr(capsys)
    assert stdout.count('could not convert:') >= 6, stdout


def test_vertical_text_diss264page21(testdir, monkeypatch):
    source = power.DISS264_PDF
    cmd = f'-i {source} --text --pages=21'
    tests.run(cmd, monkeypatch=monkeypatch)
    # load result
    document = serializeraw.load_document(testdir.tmpdir)
    # count vertical container
    vertical_container = [
        item for item in document[0]
        if isinstance(item, iamraw.VerticalTextContainer)
    ]
    assert len(vertical_container) == 1


def test_all_single_container(testdir, monkeypatch):
    source = power.DISS143_PDF
    cmd = f'-i {source} --text --pages=25'
    tests.run(cmd, monkeypatch=monkeypatch)
    document = serializeraw.load_document(testdir.tmpdir)[0]
    assert len(document) == 22


@pytest.mark.xfail(reason='improve layout parser')
def test_regression_number(testdir, monkeypatch):
    """Last line on page 127 produces '10 2' instead of '102' as last line.

    TODO: Check where this space token comes from.
    """
    source = power.DISS406_PDF
    cmd = f'-i {source} --text --pages=127'
    tests.run(cmd, monkeypatch=monkeypatch)
    document = serializeraw.load_document(testdir.tmpdir)[0]
    lastline = document[-1].text.strip()
    assert lastline == '102'
