# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import serializeraw

import linero.cluster
import linero.lines


def work(lines: str, pages: tuple = None) -> str:
    loaded = serializeraw.load_lines(lines, pages=pages)  # pylint:disable=W0612
    return ''


def analyse_page(lines, textpositions):  # pylint:disable=W0613
    clustered = linero.cluster.run(lines, maxdiff=30.0)
    for item in clustered:
        print(item)
        print()
        print()
