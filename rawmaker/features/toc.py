#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""Table of content.

Basic structure of get_outlines: (level, title, args, children)
"""

from iamraw import Section
from iamraw import create_toc
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfdocument import PDFNoOutlines
from serializeraw import dump_toc
from utila import Command
from utila import logging


def work(document: PDFDocument):
    """Extract table of content from pdf document. If no outlines are provided
    by the document, an empty list is returned"""
    outlines = []
    try:
        outlines = document.get_outlines()
    except PDFNoOutlines:
        logging('Could not locatate any outlines')

    data = [Section(level, title) for (level, title, dest, a, se) in outlines]
    toc = create_toc(data)

    # toc to yaml
    yaml = dump_toc(toc)
    return yaml


def commandline():
    return Command('-to', '--%s' % name(), 'Extract table of content.')


def name():
    return 'toc'
