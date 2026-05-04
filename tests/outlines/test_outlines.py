# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pdfminer
import pytest
import serializeraw
import utilo
import utilotest

import rawmaker.error
import rawmaker.features.outlines


def test_outlines_from_document_no_outlines(mp, capsys):
    """Test that no outlines produces an error log"""

    def get_outlines(self):
        raise rawmaker.error.MissingOutlines()

    with mp.context():
        mp.setattr(
            pdfminer.pdfdocument.PDFDocument,
            'get_outlines',
            get_outlines,
        )
        rawmaker.features.outlines.work(hoverpower.DOCU013_PDF)

    present_inerror('error', 'outlines', captured=capsys)


def test_outlines_without_outlines():
    source = hoverpower.MASTER072_PDF
    extracted = rawmaker.features.outlines.work(source)
    # no toc extraction
    # level: 0
    # style: null
    assert len(extracted) == 21, str(extracted)


def present_inerror(*items, captured):
    # TODO: MOVE TO utilo>TEST
    # TODO: SUPPORT SINGLE STRING?
    stdout, error = captured.readouterr()
    error = error.lower()
    collected = []
    for item in items:
        if item in error:
            continue
        collected.append(item)

    if collected:
        utilo.log(stdout)
        utilo.log(error)
        for item in collected:
            utilo.error(f'missing: {item}')
    assert not collected, 'see error log'


def bachelor37(toc):
    assert len(toc) == 6
    # ensure to parse pages correctly
    pages = [item.page for item in toc.children]
    assert pages == [5, 6, 15, 22, 27, 33], str(pages)


def vim(toc):
    assert len(toc) == 2
    assert len(toc[1]) == 30


def master116(toc):
    """Hint: table of content does not matches seen table of content."""
    assert len(toc) == 16


def bachelor111(toc):
    assert len(toc) == 13


def diss264(toc):
    assert len(toc) == 14


def book173(toc):
    assert len(toc) == 18


@pytest.mark.parametrize('source, validate', [
    pytest.param(hoverpower.DOCU013_PDF, vim, id='vim'),
    pytest.param(hoverpower.BACHELOR037_PDF, bachelor37, id='bachelor37'),
    pytest.param(hoverpower.MASTER116_PDF, master116, id='master116'),
    pytest.param(hoverpower.BACHELOR111_PDF, bachelor111, id='bachelor111'),
    pytest.param(hoverpower.DISS264_PDF, diss264, id='diss264'),
    pytest.param(hoverpower.BOOK173_PDF, book173, id='book173'),
])
@utilotest.nightly
def test_outlines_validate(source, validate):
    extracted = rawmaker.features.outlines.work(source)
    toc = serializeraw.load_toc(extracted)
    assert toc
    validate(toc)


def test_outlines_docu009_argparse():
    """Some NamedDestinations are store as hexadecimal numbers. This test
    ensures, that parsing, lookup in pdf dest dict and converting the
    page number works correctly."""
    source = hoverpower.DOCU014_PDF
    extracted = rawmaker.features.outlines.work(source)
    toc = serializeraw.load_toc(extracted)
    first_level = [(item.page, item.title) for item in toc]
    expected = [
        (1, 'Concepts'),
        (1, 'The basics'),
        (2, 'Introducing Positional arguments'),
        (4, 'Introducing Optional arguments'),
        (6, 'Combining Positional and Optional arguments'),
        (10, 'Getting a little more advanced'),
        (13, 'Conclusion'),
    ]
    assert first_level == expected
