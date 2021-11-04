# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Translater: Lines
=================

Translate navigator/lines between equal layout parser configuration.
The src navigator contains more lines then the dest navigator. These
lines where completly removed.

Example
-------

src      dest       translation
0        0(0)       1d->3s
1        -          2d->4s
2        -
3        3(1)
4        4(2)
"""

import texmex


def translates(sources, destinations):
    result = []
    for src, dest in zip(sources, destinations):
        assert src.page == dest.page, f'{src.page} == {dest.page}'
        translated = translate(src, dest)
        if not translated:
            continue
        result.append((src.page, translated))
    return result


def translate(
    src: texmex.PageTextNavigator,
    dest: texmex.PageTextNavigator,
) -> list:
    """\
    >>> translate(('A', 'B', 'C', 'D'), ('A', 'B', 'C', 'D'))
    []
    >>> translate(('A', 'B', 'C', 'D', 'E'), ('A', 'C', 'D'))
    [(1, 2), (2, 3)]

    Dest contains item which are not part of source navigator
    >>> translate(('A', 'B', 'C', 'D', 'E'), ('A', 'C', 'D', 'F', 'G'))
    Traceback (most recent call last):
    ...
    ValueError: src and dest does not match together: 3 F
    """
    result = []
    left = 0
    for right, dest_item in enumerate(dest):
        collected = find(src, start=left, search=dest_item)
        if collected == -1:
            error = f'src and dest does not match together: {right} {dest_item}'
            raise ValueError(error)
        if not result and collected == right:
            left = collected + 1
            continue
        result.append((right, collected))
        left = collected + 1
    return result


def find(container, start, search):
    for index, item in enumerate(container[start:], start=start):
        if search == item:
            return index
    return -1
