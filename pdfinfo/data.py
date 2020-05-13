# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses
import json

import yaml

import pdfinfo.info
import pdfinfo.meta
import pdfinfo.pages
import pdfinfo.version


@dataclasses.dataclass
class PdfInfo:
    pages: int = None
    generator: pdfinfo.info.Generator = None
    version: pdfinfo.version.Version = None
    meta: dict = None


def dump(info: PdfInfo, ext: str = 'json') -> str:
    assert ext in ('yaml', 'json'), ext
    simple = raw(info)
    if ext == 'yaml':
        return yaml.dump(simple)
    if ext == 'json':
        return json.dumps(simple)
    return None


def raw(info: PdfInfo) -> dict:
    result = {
        'pages': info.pages,
        'generator': str(info.generator),
        'version': {
            'major': info.version.major,
            'minor': info.version.minor,
        }
    }
    if info.meta:
        result['meta'] = info.meta
    return result


def parse(path: str) -> PdfInfo:
    version = pdfinfo.version.parse(path)
    if not version:
        # invalid file
        return None
    pages = pdfinfo.pages.determine(path)
    generator = pdfinfo.info.generator(path)
    meta = pdfinfo.meta.determine(path)
    info = PdfInfo(
        pages=pages,
        version=version,
        generator=generator,
        meta=meta,
    )
    return info
