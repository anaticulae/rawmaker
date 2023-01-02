# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import sys

import pdfminer.glyphlist
import pdfminer.pdfpage
import utila

before = pdfminer.pdfpage.PDFPage.create_pages  # pylint:disable=C0103


def create_pages(document):
    try:
        yield from before(document)
    except IndexError:
        utila.error('pdfminer parsing error: IndexError')
        sys.exit(1)
    except RecursionError:
        utila.error('pdfminer parsing error: RecursionError')
        sys.exit(1)


pdfminer.pdfpage.PDFPage.create_pages = create_pages

# TODO HACK HACK HACK
# bachelor090  REGISTERED SIGN
# circlecopyrt
# pdfminer.glyphlist.glyphname2unicode['circlecopyrt'] = '\u25CF'
pdfminer.glyphlist.glyphname2unicode['circlecopyrt'] = '\r'
