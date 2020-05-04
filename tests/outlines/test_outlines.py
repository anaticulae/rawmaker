# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pdfminer
import pytest
import serializeraw
import utila

import rawmaker.error
import rawmaker.features.outlines
import tests.resources


def test_outlines_from_document_no_outlines(monkeypatch, capsys):
    """Test that no outlines produces an error log"""

    def get_outlines(self):
        raise rawmaker.error.MissingOutlines()

    with monkeypatch.context():
        monkeypatch.setattr(
            pdfminer.pdfdocument.PDFDocument,
            'get_outlines',
            get_outlines,
        )
        rawmaker.features.outlines.work(tests.resources.VIM_PDF)

    present_inerror('error', 'outlines', captured=capsys)


def test_outlines_without_outlines():
    source = tests.resources.MASTER72
    extracted = rawmaker.features.outlines.work(source)

    # no toc extraction
    assert len(extracted) < 10, str(extracted)


def present_inerror(*items, captured):
    # TODO: MOVE TO UTILA>TEST
    # TODO: SUPPORT SINGLE STRING?
    stdout, error = captured.readouterr()
    error = error.lower()
    collected = []
    for item in items:
        if item in error:
            continue
        collected.append(item)

    if collected:
        utila.log(stdout)
        utila.log(error)
        for item in collected:
            utila.error(f'missing: {item}')
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


@pytest.mark.parametrize('source, validate', [
    pytest.param(tests.resources.VIM_PDF, vim, id='vim'),
    pytest.param(tests.resources.BACHELOR37, bachelor37, id='bachelor37'),
    pytest.param(tests.resources.MASTER116, master116, id='master116'),
    pytest.param(tests.resources.BACHELOR111, bachelor111, id='bachelor111'),
])
def test_outlines_validate(source, validate):
    extracted = rawmaker.features.outlines.work(source)
    toc = serializeraw.load_toc(extracted)
    assert toc
    validate(toc)
