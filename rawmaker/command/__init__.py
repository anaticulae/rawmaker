#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""The `rawmaker` takes pdf's from the input folder an parse the raw structure
of the pdf and provide them as yaml file for further analysation-processes.

- toc:    tableofcontent
- text:   text content from pdf file
- border: determine page size and bounding boxes from page content

"""
import subprocess
from contextlib import contextmanager
from functools import wraps
from glob import glob
from multiprocessing import Process
from os import getcwd
from os import makedirs
from os.path import abspath
from os.path import exists
from os.path import isabs
from os.path import isfile
from os.path import join
from sys import argv
from sys import stdin
from threading import Thread

from pdfminer.pdfdocument import PDFDocument
from utila import FAILURE
from utila import INVALID_COMMAND
from utila import NEWLINE
from utila import SUCCESS
from utila import Command
from utila import RequiredCommand
from utila import create_parser
from utila import file_append
from utila import file_create
from utila import file_read
from utila import logging
from utila import logging_error
from utila import logging_stacktrace
from utila import parse
from utila import saveme
from utila import sources

from rawmaker import FEATURE_PATH
from rawmaker import PROCESS_NAME
from rawmaker import ROOT
from rawmaker import __version__
from rawmaker.features import commandline
from rawmaker.features import find_features
from rawmaker.reader import read

FEATURES = find_features(FEATURE_PATH)


@saveme
def main():
    commands = commandline(FEATURES)
    parser = create_parser(
        commands,
        prog=PROCESS_NAME,
        version=__version__,
        outputparameter=True,
        inputparameter=True,
    )
    args = parse(parser)

    # evaluate the verbose flag
    inputpath, output, verbose = sources(args, singleinput=True, verbose=True)
    if not inputpath and not output:
        parser.print_usage()
        return FAILURE
    todolist = todo(args)
    # TODO: Do not pass all kwargs, pass only the right one to the right module
    failure = process(
        inputpath,
        output,
        todolist,
        verbose=verbose,
        parameter=args,
    )
    return failure


def process(
        inputpath: str,
        outputpath: str,
        todo,
        verbose: bool = False,
        parameter: dict = None,
):
    parameter = {} if parameter is None else parameter
    assert inputpath, outputpath
    makedirs(outputpath, exist_ok=True)

    pdfs = []
    if isfile(inputpath):
        # Single file
        pdfs.append(inputpath)
    else:
        # Search pdf's in input folder
        pdfs.extend(glob(inputpath + '/*.pdf'))
        if not pdfs:
            # Exit rawmaker when input folder is empty
            logging_error('Empty input folder: %s' % inputpath)
            exit(FAILURE)
    ret = SUCCESS
    for pdf_path in pdfs:
        with read(pdf_path) as pdf:
            if verbose:
                logging('read: %s' % pdf_path)
            for name, _, worker in FEATURES:
                # name is not a registered commando
                if name not in todo:
                    if outputpath:
                        logging('Skipping %s' % name)
                    continue
                # compute feature
                ret += process_feature(
                    name,
                    worker,
                    pdf,
                    outputpath,
                    verbose=verbose,
                    parameter=parameter,
                )
    return ret


def process_feature(
        name: str,
        worker: callable,
        ressource: PDFDocument,
        output: str,
        verbose: bool = False,
        parameter: dict = None,
):
    """Process feature `name` with `worker` and write it to `output`

    Args:
        name(str): feature to run. Examle: toc
        worker(callable): method to run
        ressource(PDFDocument): ressource to run feature on
        output(str): path to write feature
        verbose(bool): if true, logging file operation
    Returns:
        SUCCESS or FAILURE
    """
    parameter = {} if parameter is None else parameter
    pdf = ressource
    try:
        try:
            result = worker(pdf, parameter=parameter)
        except TypeError:
            result = worker(pdf)
        if result is None:  # None, because empty string is a valid result
            logging_error('No result for %s' % name)
            logging_error('Implementation of feature `%s` is missing' % name)
            return FAILURE
        try:
            # Support multiple file output from feature
            for special_name, value in result.items():
                if not isinstance(value, str):
                    msg = 'Feature %s, file %s; must return str not %s'
                    logging_error(msg % (name, special_name, type(value)))
                    return FAILURE

                write_feature_result(
                    name,
                    output,
                    result=value,
                    special_name=special_name,
                    verbose=verbose,
                )
        except AttributeError:
            # Only single result is ready for writing
            write_feature_result(name, output, result, verbose)
        return SUCCESS
    except Exception as error:  # pylint: disable=broad-except
        logging_error('while processing %s' % name)
        logging_error(error)
        logging_stacktrace()
        return FAILURE


def write_feature_result(
        name,
        output,
        result,
        special_name='',
        verbose: bool = False,
):
    special_name = '_%s' % special_name if special_name else ''
    filename = '%s__%s%s.yaml' % (PROCESS_NAME, name, special_name)
    feature_output = join(output, filename)
    if verbose:
        logging('write: %s' % feature_output)
    # Write content to file.
    file_create(feature_output, result)


def todo(args):
    args = dict(args)
    del args['input']
    del args['output']

    if not any(args.values()):
        # run all features
        result = [key for key, value in args.items()]
    else:
        result = [key for key, value in args.items() if value]
    return result
