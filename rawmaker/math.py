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
) -> iamraw.PageContentRawFormulas:
    # use char based approach
    device = rawmaker.converter.math.MathConverter()
    interpreter = pdfminer.pdfinterp.PDFPageInterpreter(device.rsrcmgr, device)

    # Processing layout
    with utila.SkipCollector(pages) as collector:
        pdfpages = pdfminer.pdfpage.PDFPage.create_pages(document)
        for index, page in enumerate(pdfpages):
            if collector.skip(index):
                continue
            device.pageno = index
            interpreter.process_page(page)

    result = device.close_document()
    return result
