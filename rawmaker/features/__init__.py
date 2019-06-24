#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
import importlib
from os import listdir
from os.path import exists
from typing import Iterable
from typing import List
from typing import Tuple

from iamraw import Document
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.layout import LTPage
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from utila import Command
from utila import logging_error

from rawmaker.miner.mining import IAmRawConverter

FEATURE_PATH_PACKAGE = 'rawmaker.features'


# TODO: replace with utila code!
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


Name = str
CommandLineInterface = List[Command]
Worker = callable  #pylint:disable=C0103
Feature = Tuple[Name, CommandLineInterface, Worker]


def commandline(features: List[Feature]) -> List[Command]:
    """Build command line interface due iterating searched features

    Args:
        features: list of parsed features
    Returns:
        list of `Command`s
    """
    result = []
    # name, cmd, work
    for _, command, _ in features:
        commands = command()
        # one single command is iterable, testing of Iterable is not possible
        if isinstance(commands, (list, tuple)):
            # support adding commands from iterable and single command
            result.extend(commands)
        else:
            result.append(commands)
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


def process_pdfpages(document: PDFDocument) -> PDFPage:
    """Yield `PDFPAge` of every single page of `PDFDocument`"""
    assert isinstance(document, PDFDocument), type(document)
    for page in PDFPage.create_pages(document):
        yield page


def process_document(document: PDFDocument) -> Tuple[int, LTPage]:
    """Yield (pagenumber, LTPage) for every single page of `PDFDocument`"""
    assert isinstance(document, PDFDocument), type(document)
    interpreter, device = create_interpreter()
    for page in process_pdfpages(document):
        interpreter.process_page(page)
        yield (page, device.get_result())


def process_pagecontent(document: PDFDocument):
    assert isinstance(document, PDFDocument), type(document)
    for _, content in process_document(document):
        yield content
