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
import pdfminer.layout
import pdfminer.pdfpage
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

    with rawmaker.reader.read(path) as document:
        # Processing layout
        content = pdfminer.pdfpage.PDFPage.create_pages(document)

        device, interpreter = rawmaker.converter.figure.create_figure_extractor(
        )

        with utila.SkipCollector(pages) as collector:
            for number, page in enumerate(content):
                if collector.skip(number):
                    continue
                device.page = number
                interpreter.process_page(page)

    figures = device.figures()

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
