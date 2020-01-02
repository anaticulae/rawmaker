# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import pdfinfo.pages
import tests.resources


def test_pdfinfo_parse_pages():
    resource = tests.resources.TOC_PDF
    pages = pdfinfo.pages.determine(resource)

    assert pages == 27, str(pages)
