# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pdfminer
import pdfminer.layout
import pdfminer.utils
import PIL.Image
import utila

import rawmaker.figure.data


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


def create_figure_extractor():
    device = FigureConverter()
    interpreter = pdfminer.pdfinterp.PDFPageInterpreter(
        device.resources,
        device,
    )
    return device, interpreter


def extract_figure(figure) -> rawmaker.figure.data.Figure:
    content = figure._objs  #  pylint:disable=W0212
    if len(content) == 1 and isinstance(content[0], pdfminer.layout.LTImage):
        # no figure, just an image container
        return None
    scalex, scaley = 1 / figure.matrix[0], 1 / figure.matrix[3]
    bounding = (
        figure.x0 * scalex,
        figure.y0 * scaley,
        figure.x1 * scalex,
        figure.y1 * scaley,
    )

    # render figure
    mode = 'RGBA'

    width = utila.flatten([[item.bbox[0], item.bbox[2]] for item in figure])
    height = utila.flatten([[item.bbox[1], item.bbox[3]] for item in figure])

    width = utila.maxs(width)
    height = utila.maxs(height)

    width = (bounding[2] - bounding[0]) + 3
    height = (bounding[3] - bounding[1])
    offset = bounding[0], bounding[1]
    scale = scalex, scaley
    size = (int(width), int(height))

    raw = PIL.Image.new(mode, size, color=1)
    renderer = PIL.ImageDraw.Draw(raw, mode=mode)

    for item in figure:
        render(item, offset, scale, renderer)

    # add text information and image border
    # renderer.rectangle((0, 0, width, height), width=5, outline='black')
    # renderer.text((width / 2, height / 2), 'left blank', fill='black', size=34)

    result = rawmaker.figure.data.Figure(data=raw, bounding=bounding)
    return result


def render(item, offset, scale, renderer):
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
            render(expanded, (0, 200), (1.0, 1.0), renderer)
    else:
        # TODO: LOG NOT SUPPORTED
        pass
