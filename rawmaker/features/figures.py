# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import io
import typing

import iamraw
import pdfminer.layout
import pdfminer.pdfpage
import PIL.Image
import PIL.ImageDraw
import serializeraw
import utila

import rawmaker.converter.basic
import rawmaker.figure.data
import rawmaker.reader

DumpedFigureInformation = typing.List[typing.Tuple[str, bytes]]


def work(path: str, pages: tuple = None) -> DumpedFigureInformation:
    pages = sorted(pages) if pages else pages

    with rawmaker.reader.read(path) as document:
        # Processing layout
        content = pdfminer.pdfpage.PDFPage.create_pages(document)

        device, interpreter = create_figure_extractor()

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
        result.append((info, image_tobytes(figure.data)))
    return result


def image_tobytes(image) -> bytes:
    raw = io.BytesIO()
    image.save(raw, format='PNG')
    raw.seek(0)
    result = raw.getvalue()
    return result


def create_figure_extractor():
    device = FigureConverter()
    interpreter = pdfminer.pdfinterp.PDFPageInterpreter(
        device.resources,
        device,
    )
    return device, interpreter


class FigureConverter(rawmaker.converter.basic.FlippedLayoutAnalyzer):

    def __init__(self):
        super().__init__()
        self.content = []
        self.page = 0

    def receive_layout(self, ltpage):
        super().receive_layout(ltpage)
        for item in ltpage:
            self.render_pagecontent(self.page, item)

    def render_pagecontent(self, pageid, item):
        """Collect all figures."""
        if isinstance(item, pdfminer.layout.LTFigure):
            self.render_figure(item, pageid=pageid)

    def render_figure(self, item: pdfminer.layout.LTFigure, pageid: int):
        rendered = extract_figure(item)
        if rendered is None:
            return
        rendered.page = pageid
        self.content.append(rendered)

    def figures(self) -> rawmaker.figure.data.Figures:
        return self.content


def extract_figure(figure) -> rawmaker.figure.data.Figure:
    content = figure._objs  #  pylint:disable=W0212
    if len(content) == 1 and isinstance(content[0], pdfminer.layout.LTImage):
        # no figure, just an image container
        return None
    bounding = (figure.x0, figure.y0, figure.x1, figure.y1)

    # render figure
    mode = 'RGBA'
    width = (bounding[2] - bounding[0])
    height = (bounding[3] - bounding[1])
    width, height = int(width), int(height)
    size = (width, height)
    raw = PIL.Image.new(mode, size, color=1)

    # add text information and image border
    renderer = PIL.ImageDraw.Draw(raw, mode=mode)
    renderer.rectangle((0, 0, width, height), width=5, outline='black')
    renderer.text((width / 2, height / 2), 'left blank', fill='black', size=34)

    result = rawmaker.figure.data.Figure(data=raw, bounding=bounding)
    return result
