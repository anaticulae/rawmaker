#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
import importlib
from importlib.util import find_spec
from importlib.util import module_from_spec
from importlib.util import spec_from_file_location
from os import listdir
from os.path import basename
from os.path import exists
from os.path import join
from os.path import split
from sys import modules
from typing import List

from iamraw import Document
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from utila import FAILURE
from utila import SUCCESS
from utila import Command
from utila import logging
from utila import logging_error

from rawmaker import ROOT
from rawmaker.miner.mining import IAmRawConverter

FEATURE_PATH_PACKAGE = 'rawmaker.features'

REQUIRED_METHODS = {'commandline', 'work'}


def find_features(path: str):
    """Locate all feautures in given path
    """
    assert exists(path), path
    collected = [
        item.replace('.py', '')
        for item in listdir(path)
        if not '__init__' in item and item.endswith('.py')
    ]
    result = []
    for item in collected:
        current = importlib.import_module(FEATURE_PATH_PACKAGE + '.' + item,
                                          FEATURE_PATH_PACKAGE)
        try:
            result.append((current.name(), current.commandline, current.work))
        except AttributeError as exception:
            logging_error('SKIP LOADING %s' % item)
            logging_error(exception)

    return result


def commandline(features):
    result = []

    # name, cmd, work
    for _, command, _ in features:
        result.append(command())

    return result


DEFAULT_PARSER_CONFIG = LAParams()


def parse_document(document: PDFDocument) -> Document:
    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()

    device = IAmRawConverter(rsrcmgr, laparams=DEFAULT_PARSER_CONFIG)
    device.new_document()
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Processing layout
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
    document = device.finish_document()
    return document


def create_interpreter() -> PDFPageInterpreter:
    rsrcmgr = PDFResourceManager()
    device = PDFPageAggregator(rsrcmgr, laparams=DEFAULT_PARSER_CONFIG)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    return interpreter, device


def process_document(document: PDFDocument):
    assert isinstance(document, PDFDocument), type(document)
    interpreter, device = create_interpreter()
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        yield (page, device.get_result())
