# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Destination
===========

Hint: There is no direct link between `Annotation` a the real pdf page.
Therefore we have to extract the reference and link them with the
page-header to determine the real pdf page. See: `pageids` and
`solve_pageid.`

Types:

- Simple: Page Number is directly encoded
- Named: Solve `Destination` reference to determine page number
- Explicit: PDFPageReference is given
"""

import contextlib
import dataclasses

import pdfminer.pdfpage


class DestinationMixin:
    pass


@dataclasses.dataclass
class ExplicitDestination(DestinationMixin):
    page: int = None
    left: float = None
    top: float = None
    zoom: float = None


@dataclasses.dataclass
class NamedDestination(DestinationMixin):
    reference: str = None

    @property
    def pdf_reference(self) -> bytes:
        """Convert human readable reference to pdf reference.

        >>> NamedDestination('Kapitel 1').pdf_reference
        b'Kapitel 1'
        """
        return self.reference.encode('ascii')


def parse(item, pagelookup: dict = None) -> ExplicitDestination:
    fitr = parse_fitr(item)
    if fitr:
        return fitr

    simple = parse_simple(item)
    if simple:
        return simple
    try:
        explicit = parse_explict(item.resolve())
    except AttributeError:
        explicit = parse_explict(item)
    if explicit:
        if pagelookup:
            explicit.page = pagelookup[explicit.page]
        return explicit

    explicit = parse_named(item)
    if explicit:
        if pagelookup:
            explicit.page = pagelookup[explicit.page]
        return explicit
    return None


def parse_simple(item):
    # Page number is directly encoded, therefore we can convert and
    # return. Example: # {'S': /'GoTo', 'D': b'0'}
    with contextlib.suppress(TypeError, AttributeError):
        page = item['D'].decode('ascii')
        return ExplicitDestination(page=page)
    return None


def parse_fitr(item):
    with contextlib.suppress(AttributeError):
        item = item.resolve()
    try:
        item = item['D']
    except TypeError:
        return None
    # {'S': /'GoTo', 'D': [0, /'FitR', 0, 625, 440, 309]}
    # [0, /'FitR', 0, 625, 440, 309]
    with contextlib.suppress(TypeError, AttributeError, IndexError):
        if item[1].name == 'FitR':
            return ExplicitDestination(page=item[0])
    return None


def parse_explict(item) -> ExplicitDestination:
    with contextlib.suppress(KeyError):
        item = item['D']

    if isinstance(item, bytes):
        # {'S': /'GoTo', 'D': b'subsection.A.5.4'}
        return None

    try:
        page, _, left, top, zoom = item  # TODO: FLIP Y-Coordinate
    except ValueError:
        return None

    with contextlib.suppress(AttributeError):
        # skip when zoom is already a float
        if zoom.name == b'null':
            zoom = 0.0

    result = ExplicitDestination(
        page=page.objid,
        left=left,
        top=top,
        zoom=zoom,
    )
    return result


def parse_named(item) -> ExplicitDestination:
    doc = item.doc
    item = item.resolve()
    with contextlib.suppress(KeyError):
        item = item['D']
    resolved = doc.lookup_name('Dests', item).resolve()
    return parse_explict(resolved)


def pageids(path: str) -> dict:
    result = {}
    with open(path, mode='rb') as pdf:
        pages = pdfminer.pdfpage.PDFPage.get_pages(
            pdf,
            check_extractable=False,
        )
        for index, page in enumerate(pages):
            result[page.pageid] = index
    return result
