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

import iamraw
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

    utila.log(f'latex:   {latex_detected}')
    utila.log(f'word:    {word_detected}')
    utila.log(f'crossed: {crossed_detected}')

    result = select_best(latex, word, crossed)
    return result


def select_best(latexs, words, crosseds) -> iamraw.PageContentTableBoundings:
    result = []
    synced = utila.sync_pages([latexs, words, crosseds], numbers=False)
    for latex, word, crossed in synced:
        selected = select_page(latex, word, crossed)
        result.append(selected)
    return result


def select_page(latex, word, crossed):
    latex = latex or []
    word = word or []
    crossed = crossed or []

    latex_detected = len(latex)
    word_detected = len(word)
    crossed_detected = len(crossed)

    result = crossed
    if word_detected > crossed_detected:
        result = word
    if latex_detected > word_detected and latex_detected > crossed_detected:
        result = latex
    return result
