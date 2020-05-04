#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""Table of content.

Basic structure of get_outlines: (level, title, args, children)
"""

from iamraw import Section
from iamraw import create_toc
from pdfminer.pdfdocument import PDFNoOutlines
from serializeraw import dump_toc
from utila import error

from rawmaker.reader import read


def work(document: str) -> str:
    """Extract table of content from pdf document. If no outlines are provided
    by the document, an empty list is returned"""
    assert isinstance(document, str), str(document)
    outlines = []
    with read(document) as pdf:
        try:
            # extract all outlines from pdf
            outlines = list(pdf.get_outlines())
        except PDFNoOutlines:
            error('Could not locatate any outlines')

    data = [Section(level, title) for (level, title, dest, a, se) in outlines]
    toc = create_toc(data)

    # toc to yaml
    yaml = dump_toc(toc)
    return yaml
