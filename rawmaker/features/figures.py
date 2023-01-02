# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Figure Extractor

Extract figures and convert to images
"""

DumpedFigureInformation = list[tuple[str, bytes]]


def work(  # pylint:disable=keyword-arg-before-vararg,W0613
    path: str,
    boxes: str = None,  # pylint:disable=W0613
    *images: list,
    pages: tuple = None,
) -> DumpedFigureInformation:
    dumped = []
    return dumped
