# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import pdfminer.pdfpage

import rawmaker.reader


@functools.lru_cache(128)
def determine(path: str) -> int:
    with rawmaker.reader.read(path) as document:
        pages = list(pdfminer.pdfpage.PDFPage.create_pages(document))
    result = len(pages)
    return result
