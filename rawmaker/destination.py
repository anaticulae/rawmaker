# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
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
import pdfminer.pdftypes

import rawmaker.utils


class DestinationMixin:
    pass


@dataclasses.dataclass
class ExplicitDestination(DestinationMixin):
    page: int = None
    left: float = None
    top: float = None
    zoom: float = None


@dataclasses.dataclass
class ExternalLinkDestination(DestinationMixin):
    """Hyperlink to external web resource.

    See: 12.6.4.7 URI Actions; PDF 2008
    """
    hyperlink: str = None


@dataclasses.dataclass
class NamedDestination(DestinationMixin):
    reference: str = None

    @property
    def pdf_reference(self) -> bytes:
        """Convert human readable reference to pdf reference.

        >>> NamedDestination('Kapitel 1').pdf_reference
        b'Kapitel 1'
        """
        encoded = rawmaker.utils.guess_encoding(self.reference)
        return encoded


def parse(item) -> DestinationMixin:  # pylint:disable=R1260
    """\
    A `null` value means that parameter shall be unchanged.

    # TODO: Change null later
    >>> parse([b'/null', 0.0, 0.0, 1.0]).page
    0
    """
    item = rawmaker.utils.resolve(item)
    hyperlink = parse_hyperlink(item)
    if hyperlink:
        return hyperlink
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


def parse_hyperlink(item) -> ExternalLinkDestination:
    """\
    >>> parse_hyperlink("{'S': /'URI', 'URI': b'http://www.helm.org/jst.pdf'}")
    """
    if not isinstance(item, dict):
        return None
    try:
        hyperlink = item['URI']
    except KeyError:
        return None
    return ExternalLinkDestination(hyperlink=hyperlink)


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
    reference = item['D']
    reference = rawmaker.utils.guess_decoding(reference)
    return NamedDestination(reference=reference)


def parse_fitr(item) -> ExplicitDestination:
    """\
    >>> from pdfminer.psparser import PSLiteral as PS
    >>> parse_fitr({'S': 'GoTo', 'D': [5, PS('FitR'), 0, 625, 440, 309]}).page
    5
    >>> parse_fitr({'D': [None, 'FitH', 3512], 'S': 'GoTo'})
    ExplicitDestination(page=0, left=None, top=3512, zoom=None)
    """
    item = rawmaker.utils.resolve(item)
    # {'S': /'GoTo', 'D': [0, /'FitR', 0, 625, 440, 309]}
    with contextlib.suppress(TypeError):
        item = item['D']
    # [0, /'FitR', 0, 625, 440, 309]
    if not isinstance(item, list):
        return None
    if isinstance(item[1], float):
        # [/b'null', 0.0, 0.0, 1.0]
        return ExplicitDestination(page=int(item[1]))  # TODO: HACK?
    fit = ('Fit', 'FitH', 'FitR', 'XYZ')
    if not item[1] in fit and not item[1].name in fit:
        return None
    pagenumber = item[0]
    top = item[2] if len(item) >= 3 else None
    if pagenumber is None:
        # TODO: CHANGE TO UNCHANGED/NONE
        pagenumber = 0
    return ExplicitDestination(page=pagenumber, top=top)


def parse_explict(item) -> ExplicitDestination:
    item = rawmaker.utils.resolve(item)
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
        # null means: do not change current zoom
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
    item = rawmaker.utils.resolve(item)
    with contextlib.suppress(KeyError):
        item = item['D']
    resolved = doc.lookup_name('Dests', item)
    resolved = rawmaker.utils.resolve(resolved)
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
