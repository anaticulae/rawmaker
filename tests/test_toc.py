# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pdfminer.layout import LAParams

from rawmaker import read
from rawmaker.error import MissingOutlines
from rawmaker.features.text import extract_content
from rawmaker.features.toc import work
from tests.resource import TOC_PDF
from tests.resource import VIM_GUIDE_PDF


def test_toc_from_document_no_outlines(monkeypatch):
    """Remove outlines from pdf document"""

    def get_outlines():
        raise MissingOutlines()

    with monkeypatch.context():
        with read(VIM_GUIDE_PDF) as document:
            document.get_outlines = get_outlines
            work(document)


def test_toc_parameterization():
    """Test parameterization to get good result when parsing table of content

    This test is more for finding a good parameter, than for realy testing.
    TODO: Improve this later. Don't know how to, yet.
    """
    with read(TOC_PDF) as pdf:
        # Diff between chars which build a word
        layout = LAParams(char_margin=10.0)
        document = extract_content(pdf, layout_parameter=layout)
    page_with_toc = document[2]
    assert page_with_toc
