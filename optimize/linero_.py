#!/usr/bin/env python
# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import hoverpower
import serializeraw
import utilo

import rawmaker

CHAR_MARGIN = utilo.ranged_exp(0.1, 50, steps=8)
WORD_MARGIN = utilo.ranged_exp(0.1, 80, steps=12)
LINE_MARGIN = utilo.ranged_exp(0.01, 2.0, steps=5)


def score(result, parameter) -> float:  # pylint:disable=W0613,C0103
    # scored = 2 * x * y
    return result


def run(path: str, char_margin: float, word_margin: float, line_margin: float):
    cmd = (f'rawmaker -i {hoverpower.BACHELOR056_PDF} --pages=15 '
           f'--char_margin={char_margin} --word_margin={word_margin} '
           f'--line_margin={line_margin} '
           '--text --line')
    utilo.run(cmd, cwd=path)
    utilo.run('tablero', cwd=path)
    loaded = serializeraw.load_tables(path)
    utilo.log(f'>>> {len(loaded)}')
    return len(loaded)


def present(result):
    for item in result:
        utilo.log(item)


if __name__ == "__main__":
    TMPDIR = utilo.tmpdir(rawmaker.ROOT)
    utilo.log(TMPDIR)
    utilo.run(
        f'optimo -i {os.path.abspath(__file__)} -VV -j=8',
        cwd=TMPDIR,
        live=True,
    )
