# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses
import json

import pdfinfo.info
import pdfinfo.pages
import pdfinfo.version


@dataclasses.dataclass
class PdfInfo:
    pages: int = None
    generator: pdfinfo.info.Generator = None
    version: pdfinfo.version.Version = None


def jsonify(info: PdfInfo) -> str:
    raw = {
        'pages': str(info.pages),
        'generator': str(info.generator),
        'version': {
            'major': info.version.major,
            'minor': info.version.minor,
        }
    }
    result = json.dumps(raw)
    return result


def parse(path: str) -> PdfInfo:
    version = pdfinfo.version.parse(path)
    if not version:
        # invalid file
        return None
    pages = pdfinfo.pages.determine(path)
    generator = pdfinfo.info.generator(path)

    info = PdfInfo(
        pages=pages,
        version=version,
        generator=generator,
    )
    return info
