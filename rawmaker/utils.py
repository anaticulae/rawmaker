# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib

import utila


def resolve(reference):
    with contextlib.suppress(AttributeError):
        return reference.resolve()
    return reference


ENCODINGS = utila.splititems('utf8 ascii cp1252')


def guess_decoding(text: bytes) -> str:
    r"""\
    >>> guess_decoding(b'http://road.cc/measure-\x96-smart-street')
    'http://road.cc/measure-–-smart-street'
    """
    for encoding in ENCODINGS:
        try:
            text = text.decode(encoding)
        except UnicodeDecodeError:
            continue
        return text
    return None
