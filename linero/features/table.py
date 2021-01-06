# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Table Extractro
===============

TODO: MOVE TO LINTER

Some tables contains double lines which indicates that is something wrong.

Example:

    If you add in word a table line and do not add any content add minize the
    height of the line with your cursor.
    Indicates that table are styled different.

"""

import serializeraw

import linero.table.strategy


def work(
        text: str,
        textposition: str,
        lines: str,
        pages: tuple = None,
) -> str:
    lines = serializeraw.load_lines(lines, pages=pages)

    navigators = serializeraw.create_pagetextnavigators_fromfile(
        text,
        textposition,
        pages=pages,
    )

    result = linero.table.strategy.run(lines, navigators)

    # remove empty pages
    result = [item for item in result if item.content]

    dumped = serializeraw.dump_tables(result)
    return dumped
