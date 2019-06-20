# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Add parser to parse non annotated links to inform user about
broken/malformated links."""
from contextlib import suppress
from dataclasses import dataclass
from enum import Enum
from typing import List
from typing import Tuple

from iamraw import BoundingBox
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from utila import Flag
from utila import from_raw_or_path
from utila import logging_error
from utila.utils import UTF8
from yaml import FullLoader
from yaml import dump
from yaml import load

from rawmaker.features import process_pdfpages


def work(document: PDFDocument):
    annotations = extract_annotations(document)
    dumped = dump_annotations(annotations)

    return {
        'annotations': dumped,
    }


class Link(Enum):
    UNDEFINED = -1
    INTERNAL = 0
    HYPERLINK = 1


@dataclass
class Annotation:
    goal: str
    bounds: BoundingBox
    typ: Link = Link.UNDEFINED


@dataclass
class HyperLink(Annotation):
    typ: Link = Link.HYPERLINK


@dataclass
class PageLink(Annotation):
    typ: Link = Link.INTERNAL


PageAnnotation = Tuple[List[PageLink], List[HyperLink]]
PageAnnotations = List[PageAnnotation]


def extract_annotations(document: PDFDocument) -> PageAnnotations:
    result = []
    for page in process_pdfpages(document):
        parsed = parse_page(page)
        result.append(parsed)
    return result


def hyperlink_annotations(annotations: PageAnnotations) -> List[HyperLink]:
    return [item[1] for item in annotations]


def pagelink_annotations(annotations: PageAnnotations) -> List[PageLink]:
    return [item[0] for item in annotations]


def parse_page(page: PDFPage):
    """Parse annoation from `PDFPage`

    There are 2 different types of annotation, the internal and external
    links.

        The internal links, better called page links refer to a chapter or
    a location in the document.
        The external links, so called hyperlink refer
    to clickable weblinks.

    # Internal reference
    # {'A': {'S': /'GoTo', 'D': b'subsection.1.30.7'}}
    # {'S': /'GoTo', 'D': b'chapter*.1'}

    Args:
        page(PDFPage):
    Returns:

    """
    if not page.annots:
        return [[], []]

    pagelinks, hyperlinks = [], []

    for reference in page.annots:
        pageobject = page.doc.getobj(reference.objid)
        bounds = BoundingBox.from_list(pageobject['Rect'])
        typ = pageobject['Type'].name
        assert typ == ANNOTATION_LABEL, typ
        annotated = pageobject['A']

        with suppress(KeyError):
            hyperlink = annotated['URI'].decode(UTF8)
            hyperlinks.append(HyperLink(bounds=bounds, goal=hyperlink))
            continue

        with suppress(KeyError):
            try:
                pagelink = annotated['D'].decode(UTF8)
            except AttributeError:
                # TODO: don't know what this element means
                #{'Type': /'Annot', 'Border': [0, 0, 0], 'H': /'I', 'C': [0,
                #0.5, 0.5], 'Rect': [348.517, 428.927, 431.794, 439.831],
                #'Subtype': /'Link', 'A': {'F': b'distributions.pdf', 'S':
                #/'GoToR', 'D': [0, /'Fit']}} [0, /'Fit']
                pagelink = str(annotated['D'])
            pagelinks.append(PageLink(bounds=bounds, goal=pagelink))
            continue
        logging_error('Unhandeld annotation %s' % pageobject)

    return [pagelinks, hyperlinks]


ANNOTATION_LABEL = 'Annot'

HYPERLINK = 'Type'
PAGE_LINK = 'S'


def dump_annotations(annotations: PageAnnotations) -> str:
    raw = []
    for page in annotations:
        pagelink, hyperlink = [], []
        if page:
            pagelink, hyperlink = page

        rawpage = [{
            'goto': link.goal,
            'bounds': link.bounds.raw(),
        } for link in pagelink]

        rawhyper = [{
            'href': link.goal,
            'bounds': link.bounds.raw(),
        } for link in hyperlink]

        raw.append([
            rawpage,
            rawhyper,
        ])
    dumped = dump(raw)
    return dumped


def load_annotations(content: str) -> PageAnnotations:
    content = from_raw_or_path(content, ftype='yaml')
    loaded = load(content, Loader=FullLoader)
    result = []
    for page in loaded:
        pagelinks = [
            PageLink(
                goal=item['goto'], bounds=BoundingBox.from_str(item['bounds']))
            for item in page[0]
        ]
        hyperlinks = [
            HyperLink(
                goal=item['href'], bounds=BoundingBox.from_str(item['bounds']))
            for item in page[1]
        ]
        result.append([
            pagelinks,
            hyperlinks,
        ])
    return result


def commandline():
    return Flag(longcut=name(), message='Extract border for every page.')


def name():
    return 'annotation'
