# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import linero.cluster
import linero.lines
import rawmaker.features.line


def work(lines: str, pages: tuple = None) -> str:
    loaded = rawmaker.features.line.load_lines(lines, pages=pages)


def analyse_page(lines, textpositions):
    clustered = linero.cluster.run(lines, maxdiff=30.0)
    for item in clustered:
        print(item)
        print()
        print()
