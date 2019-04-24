#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""Extract test out of pdf document to gather information"""

from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from serializeraw import dump_document
from utila import Command

from rawmaker.miner.mining import IAmRawConverter


def work(document: PDFDocument) -> str:
    """Extract strctured text out of document

    Args:
        document: pdf-document to run parsing
    Returns:
        parsed document as yaml output
    """
    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()

    device = IAmRawConverter(rsrcmgr, codec='utf8', laparams=laparams)
    device.new_document()
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Processing layout
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
    document = device.finish_document()

    dumped = dump_document(document)

    return dumped


def commandline():
    return Command('-te', '--%s' % name(), 'Extract text of document.')


def name():
    return 'text'
