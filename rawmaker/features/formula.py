# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw

import rawmaker.math
import rawmaker.reader


def work(path: str, pages: tuple = None) -> str:
    with rawmaker.reader.read(path) as pdf:
        formulas = rawmaker.math.extract_content(pdf, pages=pages)
    dumped = serializeraw.dump_rawformulas(formulas)
    return dumped
