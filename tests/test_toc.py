# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pdfminer
import pdfminer.layout

import rawmaker.error
import rawmaker.features.text
import rawmaker.features.toc
import tests.resources


def test_toc_from_document_no_outlines(monkeypatch, capsys):
    """Test that no outlines produces an error log"""

    def get_outlines(self):
        raise rawmaker.error.MissingOutlines()

    with monkeypatch.context():
        monkeypatch.setattr(
            pdfminer.pdfdocument.PDFDocument,
            'get_outlines',
            get_outlines,
        )
        # from pdfminer.pdfdocument import PDFDocument
        rawmaker.features.toc.work(tests.resources.VIM_GUIDE_PDF)
    _, error = capsys.readouterr()

    assert 'error' in error.lower(), error
    assert 'outlines' in error.lower(), error


def test_toc_parameterization():
    """Test parameterization to get good result when parsing table of content

    This test is more for finding a good parameter, than for realy testing.
    TODO: Improve this later. Don't know how to, yet.
    """
    with rawmaker.reader.read(tests.resources.TOC_PDF) as pdf:
        # Diff between chars which build a word
        layout = pdfminer.layout.LAParams(char_margin=10.0)
        document = rawmaker.features.text.extract_content(
            pdf,
            layout_parameter=layout,
        )
    page_with_toc = document[2]
    assert page_with_toc


def test_toc_without_outlines():
    source = tests.resources.MASTER_72_NOIMAGES_TOC
    extracted = rawmaker.features.toc.work(source)

    # no toc extraction
    assert len(extracted) < 10, str(extracted)
