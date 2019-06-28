#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
from typing import Tuple

from iamraw import Document
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.layout import LTPage
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

from rawmaker.miner.mining import IAmRawConverter


def default_parser_config():
    # TODO: define a good default one
    return LAParams()


def create_interpreter(layout=None) -> PDFPageInterpreter:
    if not layout:
        layout = default_parser_config()
    rsrcmgr = PDFResourceManager()
    device = PDFPageAggregator(rsrcmgr, laparams=layout)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    return interpreter, device


def process_pdfpages(document: PDFDocument) -> PDFPage:
    """Yield `PDFPAge` of every single page of `PDFDocument`"""
    assert isinstance(document, PDFDocument), type(document)
    for page in PDFPage.create_pages(document):
        yield page


def process_document(document: PDFDocument) -> Tuple[int, LTPage]:
    """Yield (pagenumber, LTPage) for every single page of `PDFDocument`"""
    assert isinstance(document, PDFDocument), type(document)
    interpreter, device = create_interpreter()
    for page in process_pdfpages(document):
        interpreter.process_page(page)
        yield (page, device.get_result())


def process_pagecontent(document: PDFDocument):
    assert isinstance(document, PDFDocument), type(document)
    for _, content in process_document(document):
        yield content
