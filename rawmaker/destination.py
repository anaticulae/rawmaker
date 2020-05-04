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
    explicit = parse_explict(item.resolve())
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


def parse_explict(item) -> ExplicitDestination:
    with contextlib.suppress(KeyError):
        item = item['D']
    try:
        page, _, left, top, zoom = item
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
        for index, page in enumerate(pdfminer.pdfpage.PDFPage.get_pages(pdf)):
            result[page.pageid] = index
    return result
