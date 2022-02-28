# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib


def resolve(reference):
    with contextlib.suppress(AttributeError):
        return reference.resolve()
    return reference


ENCODINGS = 'ascii cp1252 utf8 '.split()


def guess_decoding(text: bytes) -> str:
    r"""\
    >>> guess_decoding(b'http://road.cc/measure-\x96-smart-street')
    'http://road.cc/measure-–-smart-street'
    """
    text = resolve(text)
    for encoding in ENCODINGS:
        try:
            text = text.decode(encoding)
        except UnicodeDecodeError:
            continue
        return text
    return None


def guess_encoding(text: bytes) -> str:
    for encoding in ENCODINGS:
        try:
            text = text.encode(encoding)
        except UnicodeEncodeError:
            continue
        return text
    return None
