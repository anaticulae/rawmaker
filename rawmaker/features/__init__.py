#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import collections
import dataclasses
import typing

import iamraw
import pdfminer.converter
import pdfminer.layout
import pdfminer.pdfdocument
import pdfminer.pdfinterp
import pdfminer.pdfpage
import utila

import rawmaker.converter.basic
import rawmaker.miner.text
import rawmaker.parameter

PageContent = collections.namedtuple('PageContent', 'content, page')


def create_interpreter(layout=None) -> pdfminer.pdfinterp.PDFPageInterpreter:
    if not layout:
        layout = rawmaker.parameter.ParsingConfiguration().laparams()
    device = rawmaker.converter.basic.PageAggregator(laparams=layout)
    interpreter = pdfminer.pdfinterp.PDFPageInterpreter(
        device.resources,
        device,
    )
    return interpreter, device


def process_pdfpages(
        document: pdfminer.pdfdocument.PDFDocument,
        pages: tuple = None,
) -> pdfminer.pdfpage.PDFPage:
    """Contextmanager to yield `PDFPage` of every selected page of
    `PDFDocument`.

    Args:
        document: open pdf file
        pages: number of pages to procress, if None every page is processed
    Yields:
        PDFPage: tuple of page content and pdf page number
    """
    utila.call('process_pdfpages')
    assert isinstance(
        document,
        pdfminer.pdfdocument.PDFDocument,
    ), type(document)
    with utila.SkipCollector(pages) as collector:
        for number, page in enumerate(
                pdfminer.pdfpage.PDFPage.create_pages(document), start=0):
            if collector.skip(number):
                continue
            yield (page, number)


def process_document(
        document: pdfminer.pdfdocument.PDFDocument,
        pages=None,
) -> typing.Tuple[int, pdfminer.layout.LTPage]:
    """Yield (pagenumber, LTPage) for every selected page of `PDFDocument`"""
    assert isinstance(
        document,
        pdfminer.pdfdocument.PDFDocument,
    ), type(document)
    interpreter, device = create_interpreter()
    for content, number in process_pdfpages(document, pages=pages):
        interpreter.process_page(content)
        pagecontent = PageContent(content=device.get_result(), page=number)
        yield (content, pagecontent)


def process_pagecontent(
        document: pdfminer.pdfdocument.PDFDocument,
        pages=None,
) -> pdfminer.layout.LTPage:
    assert isinstance(
        document,
        pdfminer.pdfdocument.PDFDocument,
    ), type(document)
    for _, content in process_document(document, pages=pages):
        yield content


def page_selection(document: iamraw.Document, pages: tuple):
    assert isinstance(document, iamraw.Document), type(document)
    if pages:
        assert isinstance(pages, (list, tuple)), '%s %s' % (pages, type(pages))
        return pages
    # if pages is None, every page must processed
    return list(range(len(document.pages)))


def extract_content(
        document: pdfminer.pdfdocument.PDFDocument,
        config: rawmaker.parameter.ParsingConfiguration = None,
        converter=rawmaker.miner.text.PrecisePDFConverter,
        strip: bool = False,
        pages: tuple = None,
) -> iamraw.Document:
    """Extract content from PDF file

    Args:
        document(PDFDocument): PDF file to process
        config(ParsingConfiguration): Parameterization for layout analysis.
                                      This parameter defines how chars are
                                      matched together in words and sentences.
                                      See pdf reference documentation.
        converter(pdfminer.converter.PDFLayoutAnalyzer): how to handle
                                                         the layout extraction
        strip: removes white spaces at beginning and ending of text line
        pages: tuple of selected pages
    Returns:
        Document: parsed and layouted document
    """
    if config is None:
        config = rawmaker.parameter.ParsingConfiguration()
    assert isinstance(config, rawmaker.parameter.ParsingConfiguration), type(config) # yapf:disable

    # prepare parser
    device = converter(
        config=config,
        strip=strip,
    )
    device.new_document()
    interpreter = pdfminer.pdfinterp.PDFPageInterpreter(device.rsrcmgr, device)

    # Processing layout
    with utila.SkipCollector(pages) as collector:
        for index, page in enumerate(pdfminer.pdfpage.PDFPage.create_pages(document)): # yapf:disable
            if collector.skip(index):
                continue
            interpreter.process_page(page)
    result = device.finish_document()

    # upgrade page number
    pages = page_selection(result, pages)
    # TODO: REPLACE PAGE WITH ENDLESS ITER AND CHANGE ZIP TO ZIP_LONGEST
    for (page, pagenumber) in zip(result.pages, pages):
        page.page = pagenumber
    return result
