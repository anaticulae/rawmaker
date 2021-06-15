# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

import spacestation.serialize
import spacestation.wspace


def work(source: str, pages: tuple = None) -> typing.Tuple[str, str]:
    extracted, words = spacestation.wspace.extract(source, pages=pages)
    dumped = spacestation.serialize.dump_wspaces(extracted)
    dumped_words = spacestation.serialize.dump_words(words)
    return dumped, dumped_words
