#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""Document Outlines
=================

See PDF2008: 12.3.3 Document Outline

Basic structure of get_outlines: (level, title, args, children)

Entries of outlines dict
------------------------

Dest(str, list): destination if item was clicked/activated, not present
                 if A is present.
A(dict): Action(launch application, play sound, chaning state) Shall
         not be present if an DEST item is present
SE(dict): Reference to structure element(see Structural Hierarchy)
"""

import contextlib

import iamraw
import pdfminer.pdfdocument
import pdfminer.pdfpage
import serializeraw
import utila

import rawmaker.destination
import rawmaker.reader


def work(document: str) -> str:
    """Extract outlines of a pdf document.

    If there are no outlines provided dump empty list.
    """
    assert isinstance(document, str), str(document)
    data = []
    with rawmaker.reader.read(document) as pdf:
        try:
            # extract all outlines from pdf
            outlines = list(pdf.get_outlines())
            pagelookup = rawmaker.destination.pageids(document)
        except pdfminer.pdfdocument.PDFNoOutlines:
            outlines = []
            utila.error('could not locatate any outlines')
        for (level, title, dest, action, _) in outlines:
            try:
                page = pagenumber(action, dest, pdf)
            except (AttributeError, ValueError) as error:
                utila.error('PDF NOT FULLY SUPPORTED')
                utila.log_stacktrace()
                utila.error(error)
                continue

            if not isinstance(page, int):
                page = pagelookup[page.objid]
            assert isinstance(page, int), f'require convertion: {type(page)}'
            raw_section = iamraw.SectionRaw(
                level,
                title,
                page=page,
                raw='toc outline page',
                raw_location=-1,
            )
            data.append(raw_section)
    toc = iamraw.create_toc(data)
    try:
        # toc to yaml
        dumped = serializeraw.dump_toc(toc)
    except TypeError:
        utila.error('could not convert toc to YAML.')
        utila.error('The toc may contain indirect references, buffer, etc.')
        utila.error('Outline implementation seem not complete, yet.')
        dumped = None
    return dumped


def pagenumber(action, dest, pdf) -> rawmaker.destination.ExplicitDestination:
    parsed = None
    if action:
        parsed = rawmaker.destination.parse(action)
        if isinstance(parsed, rawmaker.destination.NamedDestination):
            resolved = pdf.get_dest(parsed.pdf_reference)
            resolved = resolve(resolved)
            parsed = rawmaker.destination.parse(resolved)
    elif dest:
        dest = resolve(dest)
        if isinstance(dest, list):
            # pdf 1.5: [<PDFObjRef:13>, /'XYZ', 72.0, 769.89, None]
            resolved = dest
        else:
            destname = dest if isinstance(dest, bytes) else dest.name
            resolved = pdf.get_dest(destname)
            if isinstance(resolved, list):
                # pdf 1.4: [<PDFObjRef:4>, /'XYZ', 134.031754, 373.949829, None]
                pass
            else:
                resolved = resolved.resolve()
        parsed = rawmaker.destination.parse(resolved)
    assert parsed
    if isinstance(parsed, rawmaker.destination.ExternalLinkDestination):
        return -1
    return parsed.page


def resolve(reference):
    with contextlib.suppress(AttributeError):
        return reference.resolve()
    return reference
