#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
from collections import namedtuple
from typing import Tuple

from iamraw import Document
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.layout import LTPage
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from utila import call
from utila import debug

from rawmaker.miner.mining import IAmRawConverter
from rawmaker.utils import SkipCollector

PageContent = namedtuple('PageContent', 'content, page')


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


def process_pdfpages(document: PDFDocument, pages=None) -> PDFPage:
    """Contextmanager to yield `PDFPage` of every selected page of
    `PDFDocument`.

    Args:
        document:
        pages: number of pages to procress, if None every page is processed
    Returns:
        selected pages
    """
    call('process_pdfpages')
    assert isinstance(document, PDFDocument), type(document)

    with SkipCollector(pages) as collector:
        for number, page in enumerate(PDFPage.create_pages(document), start=0):
            if collector.skip(number):
                continue
            yield (page, number)


def process_document(document: PDFDocument, pages=None) -> Tuple[int, LTPage]:
    """Yield (pagenumber, LTPage) for every selected page of `PDFDocument`"""
    assert isinstance(document, PDFDocument), type(document)
    interpreter, device = create_interpreter()
    for content, number in process_pdfpages(document, pages=pages):
        interpreter.process_page(content)
        pagecontent = PageContent(content=device.get_result(), page=number)
        yield (content, pagecontent)


def process_pagecontent(document: PDFDocument, pages=None) -> LTPage:
    assert isinstance(document, PDFDocument), type(document)
    for _, content in process_document(document, pages=pages):
        yield content


def page_selection(document: Document, pages):
    assert isinstance(document, Document), type(document)
    if pages:
        return pages
    # if pages is None, every page must processed
    return list(range(len(document.pages)))


def extract_content(
        document: PDFDocument,
        layout_parameter: LAParams = None,
        pages: list = None,
) -> Document:
    """Extract content from PDF file

    Args:
        document(PDFDocument): PDF file to process
        layout_parameter(LAParams): Parameterization for layout analysis. This
                                    parameter defines how chars are matched
                                    together in words and sentences.
                                    See pdf reference documentation.
    Returns:
        Document: parsed and layouted document
    """
    # prepare parser
    interpreter, device = setup_parser(layout_parameter)
    # Processing layout
    extracted = process_pages(document, pages, interpreter, device)
    return extracted


def setup_parser(layout_parameter):
    if layout_parameter is None:
        layout_parameter = LAParams()
    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()

    device = IAmRawConverter(rsrcmgr, laparams=layout_parameter)
    device.new_document()
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    return interpreter, device


def process_pages(document, pages, interpreter, device):
    call('process_pages')
    # Processing layout
    with SkipCollector(pages) as collector:
        for index, page in enumerate(PDFPage.create_pages(document)):
            if collector.skip(index):
                continue
            interpreter.process_page(page)
    document = device.finish_document()
    # upgrade page number

    pages = page_selection(document, pages)
    # TODO: REPLACE PAGE WITH ENDLESS ITER AND CHANGE ZIP TO ZIP_LONGEST
    for (page, pagenumber) in zip(document.pages, pages):
        page.number = pagenumber
    return document
