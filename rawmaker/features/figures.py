# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

import iamraw
import serializeraw
import utila

import rawmaker.converter.basic
import rawmaker.converter.figure
import rawmaker.figure.data
import rawmaker.figure.utils
import rawmaker.reader

DumpedFigureInformation = typing.List[typing.Tuple[str, bytes]]


def work(path: str, pages: tuple = None) -> DumpedFigureInformation:
    pages = sorted(pages) if pages else pages

    figures = rawmaker.converter.figure.extract_figures(path, pages=pages)

    dumped = dump_figures(figures)
    return dumped


def dump_figures(figures) -> DumpedFigureInformation:
    result = []
    for figure in figures:
        width = figure.bounding[2] - figure.bounding[0]
        height = figure.bounding[3] - figure.bounding[1]
        width, height = utila.roundme(width, height)
        info = iamraw.ImageInformation(
            page=figure.page,
            width=width,
            height=height,
        )
        info = serializeraw.dump_image_info(info)
        result.append((info, rawmaker.figure.utils.image_tobytes(figure.data)))
    return result
