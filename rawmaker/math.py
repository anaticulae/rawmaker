# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import pdfminer.pdfdocument
import pdfminer.pdfinterp
import pdfminer.pdfpage
import utila

import rawmaker.converter.math


def extract_content(
        document: pdfminer.pdfdocument.PDFDocument,
        pages: tuple = None,
) -> iamraw.Document:
    """Extract content from PDF file."""
    # use char based approach
    device = rawmaker.converter.math.MathConverter()
    interpreter = pdfminer.pdfinterp.PDFPageInterpreter(device.rsrcmgr, device)

    # Processing layout
    with utila.SkipCollector(pages) as collector:
        pdfpages = pdfminer.pdfpage.PDFPage.create_pages(document)
        for index, page in enumerate(pdfpages):
            if collector.skip(index):
                continue
            interpreter.process_page(page)
        # update pdf page numbers for selected pages
        length = len(list(pdfpages))
        pages = utila.ranged_tuple(0, length) if pages is None else pages

    closed = device.close_document()

    result = []
    for pagecontent, page in zip(closed, pages):
        for item in pagecontent.content:
            # set page number for every extracted formula
            item.page = page
        result.append(
            iamraw.PageContentRawFormula(
                content=pagecontent.content,
                page=page,
            ))
    return result
