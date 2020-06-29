# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import math

import iamraw
import pdfminer
import pdfminer.layout
import pdfminer.utils
import PIL.Image
import utila

import rawmaker.miner.images


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

    def figures(self) -> iamraw.Figures:
        return self.content


def extract_figures(
        document: str,
        pages: tuple = None,
) -> iamraw.Figures:
    with rawmaker.reader.read(document) as pdf:
        # Processing layout
        content = pdfminer.pdfpage.PDFPage.create_pages(pdf)

        device = FigureConverter()
        interpreter = pdfminer.pdfinterp.PDFPageInterpreter(
            device.resources,
            device,
        )

        with utila.SkipCollector(pages) as collector:
            for number, page in enumerate(content):
                if collector.skip(number):
                    continue
                device.page = number
                interpreter.process_page(page)

    figures = device.figures()
    return figures


def extract_figure(figure) -> iamraw.Figure:
    content = figure._objs  #  pylint:disable=W0212
    if len(content) == 1 and isinstance(content[0], pdfminer.layout.LTImage):
        # TODO: CHECK THIS
        # no figure, just an image container
        return None
    # TODO: Investigate about correct scaling.
    scalex, scaley = 4, 4
    # scalex, scaley = 1 / figure.matrix[0], 1 / figure.matrix[3]
    if scalex < 0 or scaley < 0:
        # TODO: DONT KNOW WHY THIS CAN HAPPEN?
        # TODO: INDICATE THIS FOR SOME USER DEFINED LAYOUT ERROR?
        utila.error(f'negative scaling: {scalex} {scaley}')
        scalex, scaley = math.fabs(scalex), math.fabs(scaley)

    bounding = scale_bounding(
        (figure.x0, figure.y0, figure.x1, figure.y1),
        (scalex, scaley),
    )

    # render figure
    mode = 'RGBA'

    width = utila.flatten([[item.bbox[0], item.bbox[2]] for item in figure])
    height = utila.flatten([[item.bbox[1], item.bbox[3]] for item in figure])

    width = utila.maxs(width)
    height = utila.maxs(height)

    width = (bounding[2] - bounding[0])
    height = (bounding[3] - bounding[1])
    offset = bounding[0], bounding[1]
    scale = scalex, scaley

    # ensure positive figure size
    if width < 0 or height < 0:
        utila.error(f'negative figure size: {width} {height}')
    width = utila.maxs(width, 1)
    height = utila.maxs(height, 1)
    size = (int(width), int(height))

    raw = PIL.Image.new(mode, size, color=1)
    renderer = PIL.ImageDraw.Draw(raw, mode=mode)

    for item in figure:
        render(item, offset, scale, renderer, raw)

    # scale bounding information to pdf size
    bounding = scale_bounding(bounding, (1.0 / scalex, 1.0 / scaley))

    result = iamraw.Figure(data=raw, bounding=bounding)
    return result


def render(item, offset, scale, renderer, rawbuffer):  # pylint:disable=R0914
    scalex, scaley = scale
    bounding = list(item.bbox)
    bounding[0] *= scale[0]
    bounding[2] *= scale[0]
    bounding[1] *= scale[1]
    bounding[3] *= scale[1]

    bounding[0] -= offset[0]
    bounding[2] -= offset[0]
    bounding[1] -= offset[1]
    bounding[3] -= offset[1]

    if isinstance(item, pdfminer.layout.LTLine):
        renderer.line(
            bounding,
            width=utila.maxs(int(item.linewidth), 1),
            fill='black',
        )
    elif isinstance(item, pdfminer.layout.LTRect):
        renderer.rectangle(
            bounding,
            width=utila.maxs(int(item.linewidth), 1),
            outline='black',
        )
    elif isinstance(item, pdfminer.layout.LTCurve):
        for current, after in zip(item.pts[0:-1], item.pts[1:]):
            expanded = pdfminer.layout.LTLine(
                linewidth=item.linewidth,
                p0=current,
                p1=after,
            )
            # TODO: 200 HACK FOR NOT FLIPPED COORDINATE
            render(expanded, (0, 200), (1.0, 1.0), renderer, rawbuffer)
    elif isinstance(item, pdfminer.layout.LTFigure):
        # render image
        images = item._objs[:]  # pylint:disable=W0212
        for image in images:
            render(image, offset, scale, renderer, rawbuffer)
    elif isinstance(item, pdfminer.layout.LTImage):
        raw = rawmaker.miner.images.image_fromlt(item)
        size = (int(item.width * scalex), int(item.height * scaley))
        location = (int(item.x0 * scalex), int(item.y0 * scaley))
        resized = raw.resize(size, resample=PIL.Image.ANTIALIAS)
        rawbuffer.paste(resized, location)
    else:
        # TODO: LOG NOT SUPPORTED
        pass


def scale_bounding(bounding: tuple, scale: tuple) -> tuple:
    result = (
        bounding[0] * scale[0],
        bounding[1] * scale[1],
        bounding[2] * scale[0],
        bounding[3] * scale[1],
    )
    return result
