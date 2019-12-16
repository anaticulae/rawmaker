# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import enum

import rawmaker.reader


class Generator(enum.Enum):
    Undefined = enum.auto()
    Latex = enum.auto()
    MSWord = enum.auto()

    def __str__(self):
        return str(self.name).lower()


def generator(path: str) -> Generator:
    with rawmaker.reader.read(path) as document:
        info = document.info[0]
    result = parse_generator(info)
    return result


def parse_generator(info):
    producer = str(info['Producer']).lower()
    if 'latex' in producer or 'tex' in producer:
        return Generator.Latex
    if 'msword' in producer or 'word' in producer:
        return Generator.MSWord
    return Generator.Undefined
