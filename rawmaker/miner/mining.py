#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
import re
import sys
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import List

from iamraw import BoundingBox
from iamraw import Char
from iamraw import Document
from iamraw import Line
from iamraw import Page
from iamraw import PageObject
from iamraw import TextContainer
from iamraw import VirtualChar
from pdfminer.converter import PDFConverter
from pdfminer.layout import LTChar
from pdfminer.layout import LTPage
from pdfminer.layout import LTTextBox


class IAmRawConverter(PDFConverter):

    CONTROL = re.compile(u'[\x00-\x08\x0b-\x0c\x0e-\x1f]')

    def __init__(self,
                 rsrcmgr,
                 codec='utf-8',
                 pageno=1,
                 laparams=None,
                 imagewriter=None,
                 stripcontrol=False):

        PDFConverter.__init__(
            self,
            rsrcmgr,
            outfp=sys.stdout.buffer,
            codec=codec,
            pageno=pageno,
            laparams=laparams)
        self.imagewriter = imagewriter
        self.stripcontrol = stripcontrol

        self.page = 0
        self.document = None

    def new_document(self):
        """Clear the current `Document` and initialze a new one"""
        self.document = Document()

    def finish_document(self) -> Document:
        """Return the current `Document` and clear the current one"""
        document = self.document
        self.document = None
        return document

    def receive_layout(self, ltpage):
        page = render(ltpage)
        self.document.pages.append(page)


@dataclass
class Lookup:

    looks: List[Any] = field(default_factory=list)

    def create(self, box: BoundingBox, **kargs):
        look = (box, kargs)
        self.looks.append(look)
        # TODO: use len?
        return self.looks.size() - 1


def render_char(item: LTChar) -> Char:
    try:
        char = Char(box=BoundingBox(*item.bbox), font=item.fontname)
        char.value = item.get_text()
    except AttributeError:
        char = VirtualChar(item.get_text())
    return char


def render_textline(item: LTTextBox):
    line = Line(BoundingBox(*item.bbox))
    for char in item._objs:  # pylint: disable=protected-access
        line.chars.append(render_char(char))  # pylint:disable=E1101
    return line


def render_textcontainer(item: LTTextBox):
    container = TextContainer(box=BoundingBox(*item.bbox))
    for line in item:
        container.lines.append(render_textline(line))  # pylint:disable=E1101
    return container


def render(item):
    if isinstance(item, LTPage):
        page = Page(item.pageid, BoundingBox(*item.bbox))
        for child in item:
            page.children.append(render(child))  # pylint:disable=E1101
        return page
    if isinstance(item, LTTextBox):
        return render_textcontainer(item)
    return PageObject(content=str(item))
