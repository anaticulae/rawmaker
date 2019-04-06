#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import subprocess
from contextlib import contextmanager
from functools import wraps
from multiprocessing import Process
from os import getcwd
from os import makedirs
from os.path import abspath
from os.path import exists
from os.path import isabs
from os.path import isfile
from os.path import join
from subprocess import PIPE
from sys import argv
from sys import stdin
from threading import Thread

from pdfminer.pdfdocument import PDFDocument
from utila import Command
from utila import create_parser
from utila import FAILURE
from utila import file_append
from utila import file_create
from utila import file_read
from utila import logging
from utila import logging_error
from utila import logging_stacktrace
from utila import NEWLINE
from utila import parse
from utila import RequiredCommand
from utila import saveme
from utila import SUCCESS

from rawmaker import __version__
from rawmaker import ROOT
from rawmaker.features import commandline
from rawmaker.features import features
from rawmaker.reader import read

INVALID_COMMAND = 2  # TODO: MOVE to utila

COMMANDS = [
    Command('-c', '--compression', 'Write complete output to one file'),
]


def stdin_reader():
    source = []
    while True:
        if stdin.closed:
            break
        try:
            data = input()
            source.append(data)
        except EOFError:
            break
        except ValueError:
            break
    return NEWLINE.join(source)


FEATURE_PATH = join(ROOT, 'rawmaker/features')
assert exists(FEATURE_PATH)

FEATURES = features(FEATURE_PATH)


@saveme
def main():
    commands = commandline(FEATURES)
    COMMANDS.extend(commands)

    parser = create_parser(
        COMMANDS,
        version=__version__,
        outputparameter=True,
        inputparameter=True,
    )
    args = parse(parser)

    inputpath, output, compression = sources(args)
    todolist = todo(args)

    failure = processing(inputpath, output, todolist, compression)

    return failure


def processing(inputpath, output, todo, compression: bool = False):
    if not inputpath:
        if output:
            logging('Reading source from stdin')
        raise NotImplemented("Reading from stdin is not supported yet.")
        source = stdin_reader()

    if output:
        makedirs(output)

    ret = 0
    with read(inputpath) as pdf:
        for name, _, worker in FEATURES:
            if name not in todo:
                if output:
                    logging('Skipping %s' % name)
                continue
            # compute feature
            ret += process_feature(name, worker, pdf, output, compression)
    return ret


def process_feature(
        name: str,
        worker: callable,
        ressource: PDFDocument,
        output: str,
        compression: bool,
):
    """Process feature `name` with `worker` and write it to `output`

    Args:
        name(str): feature to run. Examle: toc
        worker(callable): method to run
        ressource(PDFDocument): ressource to run feature on
        output(str): path to write feature
        compression(bool): If True, write everything to one file.
                           If False, write to different files, if False
                           parallelisation is possible.
    Returns:
        SUCCESS or FAILURE
    """
    pdf = ressource
    write_to_stdout = not output
    try:
        result = worker(pdf)
        if write_to_stdout:
            logging(result)
        else:
            if not compression:
                feature_output = join(output, '%s.yaml' % name)
            else:
                feature_output = join(output, 'output.yaml')
            logging('write result to: %s' % feature_output)

            # Write content to file.
            file_append(feature_output, result, create=True)
        return SUCCESS
    except Exception as error:
        logging_error('while processing %s' % name)
        logging_error(error)
        logging_stacktrace()
        return FAILURE


def todo(args):
    args = dict(args)
    del args['input']
    del args['output']
    del args['compression']

    if not any(args.values()):
        # run all features
        result = [key for key, value in args.items()]
    else:
        result = [key for key, value in args.items() if value]
    return result


def sources(args):
    cwd = abspath(getcwd())
    inputpath = args['input']
    outputpath = args['output']
    compression = args['compression']
    if inputpath:
        if not isabs(inputpath):
            # Make path absolute
            inputpath = join(cwd, inputpath)
        if not exists(inputpath):
            logging_error('Input %s does not exists' % inputpath)
            exit(INVALID_COMMAND)

    if outputpath:
        if not isabs(outputpath):
            outputpath = join(cwd, outputpath)
        if isfile(outputpath):
            logging_error('Output %s must be a directory' % outputpath)
            exit(INVALID_COMMAND)
        if exists(outputpath):
            logging_error('Output %s already exists' % outputpath)
            exit(INVALID_COMMAND)

    return (inputpath, outputpath, compression)
