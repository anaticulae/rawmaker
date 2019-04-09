#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
import re
import sys
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import List

from pdfminer.converter import PDFConverter
from pdfminer.layout import LTChar
from pdfminer.layout import LTPage
from pdfminer.layout import LTTextBox
from utila import logging_error
from utila import NEWLINE
from yaml import dump
from yaml import FullLoader
from yaml import load

INF = (1 << 31) - 1


@dataclass
class BoundingBox:
    x_bottom: float = -INF
    y_bottom: float = -INF

    x_top: float = INF
    y_top: float = INF


@dataclass
class PageObject:
    """Object to store every unsupported type"""
    box: BoundingBox = None
    content: str = None

    def dump(self):
        return ['PAGEOBJECT', self.content]


def _load_pageobject(content: str):
    return PageObject(content=content)


def _dump_pageobject(pageobject: PageObject):
    return [str(PageObject.__name__), pageobject.content]


@dataclass
class Char(PageObject):
    value: str = None
    size: float = None
    font: float = None
    style: float = None  # bold, italic, underline


def _load_char(value) -> Char:
    return Char(value=value)


def _dump_char(value: Char) -> str:
    return value.value


@dataclass
class VirtualChar():
    value: str = None
    look: int = None


@dataclass
class Page:
    number: int = 0
    dimension: BoundingBox = None
    children: List[Any] = field(default_factory=list)


def _load_page(content):
    number = content['number']
    children = content['children']

    page = Page(number)
    for class_, item_content in children:

        if class_ == TextContainer.__name__:
            page.children.append(loadme(TextContainer, item_content))

        if class_ == PageObject.__name__:
            page.children.append(loadme(PageObject, item_content))
    return page


def _dump_page(page: Page):
    result = {
        'number': page.number,
        'children': [dumper(item) for item in page.children],
    }
    return result


@dataclass
class Line(PageObject):

    chars: List[Char] = field(default_factory=list)

    @property
    def text(self) -> str:
        return ''.join([item.value for item in self.chars])

    @classmethod
    def from_str(cls, content: str):
        chars = [Char(value=item) for item in content]
        return cls(chars=chars)


def _dump_line(line: Line) -> str:
    return [Line.__class__.__name__, line.text]


def _load_line(line: str) -> Line:
    chars = []
    for char in line:
        chars.append(_load_char(value=char))
    return Line(chars=chars)


@dataclass
class TextContainer(PageObject):
    lines: List[Line] = field(default_factory=list)

    @property
    def text(self):
        return NEWLINE.join([item.text for item in self.lines])

    def dump(self):
        return [
            str(self.__class__.__name__), [item.text for item in self.lines]
        ]


def _dump_textcontainer(container: TextContainer):
    return [
        str(container.__class__.__name__),
        [item.text for item in container.lines]
    ]


def _load_textcontainer(content) -> TextContainer:

    lines = [_load_line(item) for item in content]
    return TextContainer(lines=lines)


@dataclass
class Document:
    dimension: BoundingBox = None
    pages: List[Page] = field(default_factory=list)

    @property
    def page_count(self):
        return len(self.pages)


def _load_document(content):
    document = Document()
    document.pages = [loadme(Page, item) for item in content['pages']]
    return document


def _dump_document(document: Document) -> dict:
    result = {
        'pages': [dumper(item) for item in document.pages],
    }
    return result


def dump_yaml(document: Document) -> str:
    """Convert to raw python to have more clear yaml output"""
    assert isinstance(document, Document), type(document)
    raw = dumper(document)
    return dump(raw)


def load_yaml(content: str) -> Document:
    assert isinstance(content, str)
    loaded = load(content, Loader=FullLoader)
    return loadme(Document, loaded)


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
        self.document = Document()

    def finish_document(self):
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
        return self.looks.size() - 1


def render_char(item: LTChar) -> Char:
    try:
        char = Char(box=BoundingBox(*item.bbox))
        char.value = item.get_text()
    except AttributeError:
        char = VirtualChar(item.get_text())
    return char


def render_textline(item: LTTextBox):
    line = Line(BoundingBox(*item.bbox))
    for char in item._objs:
        line.chars.append(render_char(char))
    return line


def render_textcontainer(item: LTTextBox):
    container = TextContainer(box=BoundingBox(*item.bbox))
    for line in item:
        container.lines.append(render_textline(line))
    return container


def render(item):
    if isinstance(item, LTPage):
        page = Page(item.pageid, BoundingBox(*item.bbox))
        for child in item:
            page.children.append(render(child))
        return page
    elif isinstance(item, LTTextBox):
        return render_textcontainer(item)
    else:
        return PageObject(content=str(item))


def dumper(content):
    key = content.__class__.__name__
    try:
        dumpy, _ = DUMP_LOAD[key]
    except KeyError as error:
        logging_error('Could not dump %s' % error)
        return None
    else:
        return dumpy(content)


def loadme(structure, data):
    try:
        _, loady = DUMP_LOAD[structure.__name__]
    except KeyError as error:
        logging_error('Could not load %s' % error)
        return None
    else:
        return loady(data)


DUMP_LOAD = {
    Char.__name__: (_dump_char, _load_char),
    Document.__name__: (_dump_document, _load_document),
    Line.__name__: (_dump_line, _load_line),
    Page.__name__: (_dump_page, _load_page),
    TextContainer.__name__: (_dump_textcontainer, _load_textcontainer),
    PageObject.__name__: (_dump_pageobject, _load_pageobject),
}
