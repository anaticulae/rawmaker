# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pdfminer.pdfpage
import utila

before = pdfminer.pdfpage.PDFPage.create_pages  # pylint:disable=C0103


def create_pages(document):
    try:
        yield from before(document)
    except IndexError:
        utila.error('pdfminer parsing error: IndexError')
        exit(1)
    except RecursionError:
        utila.error('pdfminer parsing error: RecursionError')
        exit(1)


pdfminer.pdfpage.PDFPage.create_pages = create_pages
