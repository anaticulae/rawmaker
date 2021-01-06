# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
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


def parse(item) -> ExplicitDestination:  # pylint:disable=R1260
    fitr = parse_fitr(item)
    if fitr:
        return fitr

    simple = parse_simple(item)
    if simple:
        return simple

    for method in (parse_explict, parse_named):
        explicit = method(item)
        if explicit:
            return explicit
    return None


def parse_simple(item) -> NamedDestination:
    """Page number is directly encoded, therefore we can convert and
    return.

    >>> from pdfminer.psparser import PSLiteral as PS
    >>> parse_simple({'S': PS('GoTo'), 'D': b'FF'}).reference
    'FF'

    """
    if not isinstance(item, dict):
        return None
    if not item['S'].name == 'GoTo':
        # 12.6.4.2 Go-To Actions
        return None
    reference = item['D'].decode('ascii')
    return NamedDestination(reference=reference)


def parse_fitr(item) -> ExplicitDestination:
    """\
    >>> from pdfminer.psparser import PSLiteral as PS
    >>> parse_fitr({'S': 'GoTo', 'D': [5, PS('FitR'), 0, 625, 440, 309]}).page
    5
    """
    with contextlib.suppress(AttributeError):
        item = item.resolve()
    # {'S': /'GoTo', 'D': [0, /'FitR', 0, 625, 440, 309]}
    with contextlib.suppress(TypeError):
        item = item['D']
    # [0, /'FitR', 0, 625, 440, 309]
    if not isinstance(item, list):
        return None
    if not item[1].name in ('Fit', 'FitR', 'XYZ'):
        return None
    pagenumber = item[0]
    return ExplicitDestination(page=pagenumber)


def parse_explict(item) -> ExplicitDestination:
    with contextlib.suppress(AttributeError):
        item = item.resolve()
    with contextlib.suppress(KeyError, TypeError):
        # KeyError: ? add docs here ?
        # TypeError: item is already the requested list:
        # [34, /'XYZ', 72.4799999, 532.319999, 0]
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
        page=page,
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
