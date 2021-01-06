# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Table Extraction Strategy
============================

TODO: Add optimal table extraction selector for every single page, cause
table style can change in document.
"""

import functools

import utila

import linero.table.crossed
import linero.table.horizontal
import linero.table.word


def run(lines, navigators):
    crossed = functools.partial(linero.table.crossed.run, lines)
    latex = functools.partial(linero.table.horizontal.run, lines, navigators)
    word = functools.partial(linero.table.word.run, lines)

    crossed, latex, word = utila.fork(crossed, latex, word, process=True)

    latex_detected = sum([len(item.content) for item in latex])
    word_detected = sum([len(item.content) for item in word])
    crossed_detected = sum([len(item.content) for item in crossed])

    result = crossed
    if word_detected > crossed_detected:
        result = word
    if latex_detected > word_detected and latex_detected > crossed_detected:
        result = latex
    return result
