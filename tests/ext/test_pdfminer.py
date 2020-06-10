#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""Ensure that basic functunality of pdfminer-six works.

The functionality is encapsulated by `rawmaker` api.
"""

import power
import pytest

import rawmaker.error
import rawmaker.reader
import tests.resources


def test_outline_count():
    """Test reading outlines from document."""
    with rawmaker.reader.read(power.DOCU13_PDF) as document:
        outlines = document.get_outlines()
        # pylint: disable=unused-variable
        # pylint: disable=invalid-name
        for (level, title, dest, reference, se) in outlines:
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
        assert section_count == tests.resources.VIM_OUTLINES


def test_read_no_pdf():
    """Reading non valid pdf. The example contains some raw text."""
    with pytest.raises(rawmaker.error.InvalidPDF):
        with rawmaker.reader.read(tests.resources.NO_PDF):
            pass
