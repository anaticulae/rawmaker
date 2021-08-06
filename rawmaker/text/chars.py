# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw

import rawmaker.features.text
import rawmaker.miner.char
import rawmaker.reader


def extract_chars(document: str, pages: tuple = None) -> iamraw.Document:
    assert isinstance(document, str), str(document)
    document = rawmaker.features.text.extract_document(
        document,
        pages=pages,
        converter=rawmaker.miner.char.CharPDFConvert,
    )
    return document
