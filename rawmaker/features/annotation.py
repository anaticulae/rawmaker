# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Add parser to parse non annotated links to inform user about
broken/malformated links."""
from contextlib import suppress

import iamraw
import pdfminer.pdfdocument
import serializeraw
import utila

from rawmaker.features import process_pdfpages
from rawmaker.reader import read


def work(document: str, pages=None) -> str:
    assert isinstance(document, str), str(document)
    if True:  # pylint:disable=using-constant-test
        # disable bad annotation parser
        return ''
    with read(document) as pdf:
        annotations = extract_annotations(pdf, pages=pages)
    dumped = serializeraw.dump_annotations(annotations)
    return dumped


def extract_annotations(
        document: pdfminer.pdfdocument.PDFDocument,
        pages=None,
) -> iamraw.PageAnnotations:
    result = []
    for page, number in process_pdfpages(document, pages=pages):
        parsed = parse_page(page, pagenumber=number)
        result.append(parsed)
    return result


ANNOTATION_LABEL = 'Annot'


def parse_page(  # pylint:disable=R1260
        page: pdfminer.pdfpage.PDFPage,
        pagenumber: int,
) -> iamraw.PageAnnotation:
    """Parse annoation from `PDFPage`.

    Args:
        page: pdf page to parse annotation
        pagenumber: number of selected page
    Returns:
        parsed Annotations.

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
    pageannotation = page.annots
    if not pageannotation:
        return iamraw.PageAnnotation(None, None, pagenumber)
    # WORKAROUND: THIS IS A FIX WHEN PAGE ANNOTATIONS ARE NESTED IN A SINGLE
    # REFERENCE, DON'T KNOW WHY THIS CAN HAPPEN. TODO: INVESTIGATE LATER
    if not isinstance(pageannotation, list):
        getobj = page.doc.getobj
        pageannotation = [item for item in getobj(page.annots.objid)]

    pagelinks, hyperlinks = [], []
    for reference in pageannotation:
        pageobject = page.doc.getobj(reference.objid)
        # TODO: FLIP Y-COORDINATE?
        # TODO: REMOVE ROUNDING AFTER PATCHING IAMRAW
        coords = [utila.roundme(item) for item in pageobject['Rect']]
        bounds = iamraw.BoundingBox.from_list(coords)
        try:
            typ = pageobject['Type'].name
        except KeyError:
            # TODO: REMOVE THIS PART OF CODE
            utila.error('skip annotation %s' % pageobject)
            continue
        assert typ == ANNOTATION_LABEL, typ
        try:
            annotated = pageobject['A']
        except KeyError:
            # TODO: WORKAORUND: INVESTIGATE LASTER
            utila.error(f'Unhandeld annotation A {pageobject}')
            continue

        if isinstance(annotated, pdfminer.pdftypes.PDFObjRef):
            # TODO: add layer to automatically convert reference to object.
            annotated = page.doc.getobj(annotated.objid)

        with suppress(KeyError):
            hyperlink = annotated['URI'].decode(utila.UTF8)
            hyperlinks.append(iamraw.HyperLink(bounds=bounds, goal=hyperlink))
            continue

        with suppress(KeyError):
            try:
                pagelink = annotated['D'].decode(utila.UTF8)
            except AttributeError:
                # TODO: don't know what this element means
                #{'Type': /'Annot', 'Border': [0, 0, 0], 'H': /'I', 'C': [0,
                #0.5, 0.5], 'Rect': [348.517, 428.927, 431.794, 439.831],
                #'Subtype': /'Link', 'A': {'F': b'distributions.pdf', 'S':
                #/'GoToR', 'D': [0, /'Fit']}} [0, /'Fit']
                pagelink = str(annotated['D'])
            pagelinks.append(iamraw.PageLink(bounds=bounds, goal=pagelink))
            continue
        utila.error('Unhandeld annotation %s' % pageobject)

    return iamraw.PageAnnotation(pagelinks, hyperlinks, page=pagenumber)
