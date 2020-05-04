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
import serializeraw
import utila

import rawmaker.reader


def work(document: str) -> str:
    """Extract outlines of a pdf document. If there are no outlines
    provided dump empty list.
    """
    assert isinstance(document, str), str(document)
    with rawmaker.reader.read(document) as pdf:
        try:
            # extract all outlines from pdf
            outlines = list(pdf.get_outlines())
        except pdfminer.pdfdocument.PDFNoOutlines:
            outlines = []
            utila.error('could not locatate any outlines')

    data = []
    for (level, title, dest, a, se) in outlines:  # pylint:disable=W0612,C0103
        data.append(iamraw.Section(level, title))

    toc = iamraw.create_toc(data)
    # toc to yaml
    yaml = serializeraw.dump_toc(toc)
    return yaml
