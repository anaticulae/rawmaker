# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Add parser to parse non annotated links to inform user about
broken/malformated links."""

import contextlib

import iamraw
import pdfminer.pdfdocument
import serializeraw
import utila

import rawmaker.features
import rawmaker.reader
import rawmaker.utils


def work(document: str, pages=None) -> str:
    assert isinstance(document, str), str(document)
    with rawmaker.reader.read(document) as pdf:
        annotations = extract_annotations(pdf, pages=pages)
    dumped = serializeraw.dump_annotations(annotations)
    return dumped


def extract_annotations(
    document: pdfminer.pdfdocument.PDFDocument,
    pages=None,
) -> iamraw.PageAnnotations:
    result = []
    for page, number in rawmaker.features.process_pdfpages(
            document,
            pages=pages,
    ):
        parsed = parse_page(page, pagenumber=number)
        if not (parsed.hyperlinks or parsed.pagelinks):
            # skip empty page
            continue
        result.append(parsed)
    return result


ANNOTATION_LABEL = 'Annot'


def parse_page(
    page: pdfminer.pdfpage.PDFPage,
    pagenumber: int,
) -> iamraw.PageAnnotation:
    """Parse annotation from `PDFPage`.

    Args:
        page(PDFPage): pdf page to parse annotation
        pagenumber(int): number of selected page
    Returns:
        parsed Annotations.

    There are 2 different types of annotation, the internal and external
    links:
    *   The internal links, better called page links refer to a chapter or a
        location in the document.
    *   The external links, so called hyperlink refer to clickable weblinks.

    # Internal reference
    # {'A': {'S': /'GoTo', 'D': b'subsection.1.30.7'}}
    # {'S': /'GoTo', 'D': b'chapter*.1'}
    """
    pageannotation = page.annots
    if not pageannotation:
        return iamraw.PageAnnotation(None, None, pagenumber)
    getobj = page.doc.getobj
    if not isinstance(pageannotation, list):
        # WORKAROUND: THIS IS A FIX WHEN PAGE ANNOTATIONS ARE NESTED IN A
        # SINGLE REFERENCE, DON'T KNOW WHY THIS CAN HAPPEN. TODO:
        # INVESTIGATE LATER
        pageannotation = list(getobj(page.annots.objid))
    pagelinks, hyperlinks = [], []
    for reference in pageannotation:
        if isinstance(reference, dict):
            # reference is already resolved
            pageobject = reference
        else:
            pageobject = getobj(reference.objid)
        reference = parse_reference(pageobject, getobj)
        if reference:
            pagelinks.append(reference)
            continue
        external = parse_external(pageobject, getobj)
        if external:
            hyperlinks.append(external)
            continue
        utila.error(f'Unhandeld annotation {pageobject}')
    # flip boundings
    pageheight = float(page.mediabox[3])
    for item in pagelinks:
        item.bounds = flip_bounding(item.bounds, pageheight)
    for item in hyperlinks:
        item.bounds = flip_bounding(item.bounds, pageheight)
    return iamraw.PageAnnotation(pagelinks, hyperlinks, page=pagenumber)


def flip_bounding(box, pageheight):
    result = iamraw.BoundingBox(
        box[0],
        pageheight - box[3],
        box[2],
        pageheight - box[1],
    )
    return result


def parse_reference(pageobject, getobj=None) -> iamraw.PageLink:
    link = parse_link(pageobject)
    if link:
        return link
    label = parse_label(pageobject, getobj)
    if label:
        return label
    return None


def parse_label(pageobject, getobj=None) -> iamraw.PageLink:
    try:
        typ = pageobject['Type'].name
        if typ != ANNOTATION_LABEL:
            return None
    except KeyError:
        return None
    try:
        annotated = pageobject['A']
    except KeyError:
        return None
    if isinstance(annotated, pdfminer.pdftypes.PDFObjRef):
        # TODO: add layer to automatically convert reference to object.
        annotated = getobj(annotated.objid)
    try:
        pagelink = annotated['D']
    except KeyError:
        return None
    bounds = determine_bounding(pageobject['Rect'])
    pagelink = parse_pagelink(pagelink)
    return iamraw.PageLink(bounds=bounds, goal=pagelink)


def parse_link(pageobject) -> iamraw.PageLink:
    # TODO: don't know what this element means
    #{'Type': /'Annot', 'Border': [0, 0, 0], 'H': /'I', 'C': [0,
    #0.5, 0.5], 'Rect': [348.517, 428.927, 431.794, 439.831],
    #'Subtype': /'Link', 'A': {'F': b'distributions.pdf', 'S':
    #/'GoToR', 'D': [0, /'Fit']}} [0, /'Fit']
    try:
        typ = pageobject['Subtype'].name
        if typ != 'Link':
            return None
        assert typ == 'Link'
    except KeyError:
        return None
    try:
        pagelink = pageobject['Dest']
    except KeyError:
        return None
    bounds = determine_bounding(pageobject['Rect'])
    pagelink = parse_pagelink(pagelink)
    return iamraw.PageLink(bounds=bounds, goal=pagelink)


def parse_external(pageobject, getobj=None) -> iamraw.HyperLink:
    try:
        annotated = pageobject['A']
    except KeyError:
        return None
    if isinstance(annotated, pdfminer.pdftypes.PDFObjRef):
        # TODO: add layer to automatically convert reference to object.
        annotated = getobj(annotated.objid)
    bounds = determine_bounding(pageobject['Rect'])
    with contextlib.suppress(KeyError):
        hyperlink = annotated['URI']
        hyperlink = hyperlink_decode(hyperlink)
        return iamraw.HyperLink(bounds=bounds, goal=hyperlink)
    return None


def hyperlink_decode(text: bytes) -> str:
    r""""
    text(bytes): 7-bit ASCII, see 12.6.4.7

    Hint: ASCII must not always be correct cause of bad programmed printer.?
    TODO: MAY A PDFMINER CONVERTION ERROR?
    TODO: VERIFY LINUX/WIN DUE CP1252

    >>> hyperlink_decode(b'http://road.cc/measure-\x96-smart-street')
    'http://road.cc/measure-–-smart-street'
    """
    result = rawmaker.utils.guess_decoding(text)
    if result is None:
        utila.error(f'annotation: could not decode: {text}')
    return result


def parse_pagelink(pagelink):
    r"""\
    >>> parse_pagelink(b'glo:glos:Glas\xfcbergangstemperatur')
    'glo:glos:Glasübergangstemperatur'
    """
    if isinstance(pagelink, bytes):
        decoded = rawmaker.utils.guess_decoding(pagelink)
        if decoded:
            return decoded
    if isinstance(pagelink, list):
        if isinstance(pagelink[0], pdfminer.pdftypes.PDFObjRef):
            # internal link to pdf page
            # resolve objid
            pagelink[0] = f'objid: {pagelink[0].objid}'
        pagelink = [str(item) for item in pagelink]
    else:
        pagelink = str(pagelink)
    return pagelink


def determine_bounding(bounding):
    bounding = utila.rectangle_ensure_bounding(bounding)
    result = iamraw.BoundingBox.from_list(bounding)
    return result
