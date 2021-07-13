# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import enum

import rawmaker.reader


class Generator(enum.Enum):
    UNDEFINED = enum.auto()
    LATEX = enum.auto()
    MSWORD = enum.auto()

    def __str__(self):
        return str(self.name).lower()


def generator(path: str) -> Generator:
    with rawmaker.reader.read(path) as document:
        try:
            info = document.info[0]
        except IndexError:
            # no editor information provided
            return Generator.UNDEFINED
    result = parse_generator(info)
    return result


def parse_generator(info):
    """\
    No `Producer` defined:
    >>> parse_generator({'Author': b'Maik Hesse', 'Title': b'Essays on Trust '
    ... b'and Reputation Portability in Digital Platform Ecosystems'})
    <Generator.UNDEFINED:...>
    """
    try:
        producer = str(info['Producer']).lower()
    except KeyError:
        return Generator.UNDEFINED
    if 'latex' in producer or 'tex' in producer:
        return Generator.LATEX
    if 'msword' in producer or 'word' in producer:
        return Generator.MSWORD
    return Generator.UNDEFINED
