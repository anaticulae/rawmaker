# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw

import pdfinfo.info
import pdfinfo.meta
import pdfinfo.pages
import pdfinfo.version


def parse(path: str) -> iamraw.PDFInfo:
    version = pdfinfo.version.parse(path)
    if not version:
        # invalid file
        return None
    pages = pdfinfo.pages.determine(path)
    generator = pdfinfo.info.generator(path)
    meta = pdfinfo.meta.determine(path)
    info = iamraw.PDFInfo(
        pages=pages,
        version=version,
        generator=generator,
        meta=meta,
    )
    return info
