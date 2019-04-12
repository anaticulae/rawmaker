#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""Table of content.

Basic structure of get_outlines: (level, title, args, children)
"""

from iamraw import Section
from iamraw import create_toc
from pdfminer.pdfdocument import PDFDocument
from serializeraw.toc import dump_yaml as dump_toc
from utila import Command


def commandline():
    return Command('-to', '--%s' % name(), 'Extract table of content.')


def work(document: PDFDocument):
    outlines = document.get_outlines()

    data = [Section(level, title) for (level, title, dest, a, se) in outlines]

    toc = create_toc(data)

    # toc to yaml
    yaml = dump_toc(toc)
    return yaml


def name():
    return 'toc'
