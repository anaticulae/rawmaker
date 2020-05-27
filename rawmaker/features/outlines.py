#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
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

import iamraw
import pdfminer.pdfdocument
import pdfminer.pdfpage
import serializeraw
import utila

import rawmaker.destination
import rawmaker.reader


def work(document: str) -> str:
    """Extract outlines of a pdf document. If there are no outlines
    provided dump empty list.
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
            outline_pagenumber = pagenumber(action, dest, pagelookup, pdf)
            raw_section = iamraw.SectionRaw(
                level,
                title,
                page=outline_pagenumber,
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


def pagenumber(action, dest, pagelookup, pdf) -> rawmaker.destination.ExplicitDestination: # yapf:disable
    parsed = None
    if action:
        parsed = rawmaker.destination.parse(action, pagelookup)
    elif dest:
        destname = dest if isinstance(dest, bytes) else dest.name
        resolved = pdf.get_dest(destname).resolve()
        parsed = rawmaker.destination.parse(resolved, pagelookup)
    assert parsed
    return parsed.page
