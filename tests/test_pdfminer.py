#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""Ensure that basic functunality of pdfminer-six works.

The functionality is encapsulated by `rawmaker` api.
"""

from pytest import raises

from rawmaker import InvalidPDF
from rawmaker import pages
from rawmaker import read
from tests.resource import NO_PDF
from tests.resource import VIM_GUIDE_OUTLINES
from tests.resource import VIM_GUIDE_PAGES
from tests.resource import VIM_GUIDE_PDF


def test_read_file():
    """Read pdf and check the size of pages"""
    with read(VIM_GUIDE_PDF) as document:
        items = list(pages(document))  # extract all pages from iterator
        assert items

        number_of_pages = len(items)
        assert number_of_pages == VIM_GUIDE_PAGES


def test_outline_count():
    """Test reading outlines from document"""
    with read(VIM_GUIDE_PDF) as document:
        outlines = document.get_outlines()
        for (level, title, dest, a, se) in outlines:
            # print(level, title, dest, a, se)
            # 1 Table of contents None <PDFObjRef:2> None
            # 1 Vim Commands None <PDFObjRef:7> None
            # 2 Starting Vim None <PDFObjRef:11> None
            # 2 Undo/Redo None <PDFObjRef:15> None
            # 2 Insert None <PDFObjRef:19> None
            # 2 Copy/Paste/Delete None <PDFObjRef:23> None
            # 2 Paste in search or colon commands None <PDFObjRef:27> None
            pass

        section_count = len(list(document.get_outlines()))
        assert section_count == VIM_GUIDE_OUTLINES


def test_read_no_pdf():
    """Reading non valid pdf.

    The example contains some raw text."""
    with raises(InvalidPDF):
        with read(NO_PDF) as fp:
            pass
