# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import pdfminer.converter
import pdfminer.image
import pdfminer.layout
import pdfminer.pdfdocument
import pdfminer.pdfinterp
import pdfminer.pdftypes
import pdfminer.psparser
import utila

import rawmaker.converter.basic


class ImageConverter(rawmaker.converter.basic.FlippedLayoutAnalyzer):

    def __init__(self, imagewriter, firstpage: int):
        super().__init__(pageno=firstpage)
        assert callable(imagewriter), imagewriter
        self.imagewriter = imagewriter
        # TODO avoid duplicated parsed, check if we require this?
        self.parsed = utila.Single()

    def receive_layout(self, ltpage):
        super().receive_layout(ltpage)
        for item in ltpage:
            self.render_pagecontent(ltpage.pageid, item)

    def render_pagecontent(self, pageid, item):
        """Collect all imageable items"""
        if isinstance(item, pdfminer.layout.LTImage):
            self.render_result_image(item, pageid=pageid)
        elif isinstance(item, pdfminer.layout.LTFigure):
            self.render_figure(item, pageid=pageid)

    def render_result_image(
        self,
        image: pdfminer.layout.LTImage,
        pageid: int,
    ):
        # add pageid to ensure that equal image names from different pages
        # are not handled as same same.
        imagename = f'{pageid}_{image.name}'
        if self.parsed.contains(imagename):
            return
        self.imagewriter(pageid, image)

    def render_figure(
        self,
        item: pdfminer.layout.LTFigure,
        pageid: int,
    ):
        # TODO: RENDER CURVES ETC.
        images = item._objs  # pylint:disable=W0212
        if len(images) == 1:
            if isinstance(images[0], pdfminer.layout.LTFigure):
                # image inside figure
                images = images[0]._objs  # pylint:disable=W0212
        images = [
            item for item in images if isinstance(item, pdfminer.layout.LTImage)
        ]
        if not images:
            return
        assert len(images) == 1, str(images)
        # TODO: Investigate with list
        image = images[0]  # pylint:disable=W0212
        if skipme(image):
            return
        self.render_result_image(image, pageid)


SKIPME_RATE_MIN = configo.HV_PERCENT_PLUS(default=50.0)


def skipme(image) -> bool:
    """\
    Master31Page10 Black/White image is printed under figure caption.
    """
    # TODO: INVESTIGATE THIS HACK
    stream_raw = image.stream.rawdata
    counted = stream_raw.count(b'\x00')
    rate = counted / len(stream_raw)
    if rate >= SKIPME_RATE_MIN:
        return True
    return False


class FastImageInterpreter(pdfminer.pdfinterp.PDFPageInterpreter):
    """Experimental, think about the sence of this ?optimization?."""

    # TODO: SEE DOCSTRING

    def __init__(self, rsrcmgr, device):
        super().__init__(rsrcmgr, device)
        self.fast = {
            'CS': self.do_CS,
            'Do': self.do_Do,
            'EI': self.do_EI,
            'MP': self.do_MP,
            'Q': self.do_Q,
            'SC': self.do_SC,
            'SCN': self.do_SCN,
            'cm': self.do_cm,
            'cs': self.do_cs,
            'sc': self.do_sc,
            'scn': self.do_scn,
        }

    # pylint:disable=W0613,R0201
    def render_char(self, matrix, font, fontsize, scaling, rise, cid, ncs,
                    graphicstate):
        # assert 0
        return

    def render_string(self, textstate, seq, ncs, graphicstate):
        return

    def do_TJ(self, seq):
        return

    def execute(self, streams):  # pylint:disable=R1260
        try:
            parser = pdfminer.pdfinterp.PDFContentParser(streams)
        except pdfminer.psparser.PSEOF:
            # empty page
            return
        while 1:
            try:
                (_, obj) = parser.nextobject()
            except pdfminer.psparser.PSEOF:
                break
            if isinstance(obj, pdfminer.psparser.PSKeyword):
                name = pdfminer.psparser.keyword_name(obj)
                try:
                    func = self.fast[name]
                except KeyError:
                    continue
                nargs = func.__code__.co_argcount - 1
                # nargs = six.get_function_code(func).co_argcount - 1
                if nargs:
                    args = self.pop(nargs)
                    if len(args) == nargs:
                        func(*args)
                else:
                    func()

            else:
                self.push(obj)


def create_fastimageextractor(imagelistener, firstpage: int):
    device = ImageConverter(
        imagewriter=imagelistener,
        firstpage=firstpage,
    )
    interpreter = pdfminer.pdfinterp.PDFPageInterpreter(
        device.resources,
        device,
    )
    return interpreter
