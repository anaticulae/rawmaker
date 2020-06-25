# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import linero.table.horizontal
import linero.table.word


def run(lines, navigators):
    latex = linero.table.horizontal.run(lines, navigators)
    word = linero.table.word.run(lines)

    latex_detected = sum([len(item.content) for item in latex])
    word_detected = sum([len(item.content) for item in word])

    result = word if word_detected >= latex_detected else latex
    return result
