#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# Tis file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
from importlib import import_module
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

from utila import Command
from utila import FAILURE
from utila import logging
from utila import logging_error
from utila import SUCCESS

import rawmaker.features
from rawmaker import ROOT

LOADED = False


def find_features(path: str):
    """Locate all feautures in given path

    Args:
        path(str): absoulte path to feature location
    Retuns:
        list of python files, which are possible features, as relative path to
        `path`
    """
    msg = 'Path does not exists %s' % path
    assert exists(path), msg

    result = [
        item for item in listdir(path)
        if not '__init__' in item and item.endswith('.py')
    ]

    result = [item.replace('.py', '') for item in result]

    return result


def features(path: str):
    features = find_features(path)
    result = []
    for item in features:
        current = import_module(FEATURE_PATH_PACKAGE + '.' + item,
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


def load_features(feature_root: str, features: List[str]):
    """Load list with possible features

    Args:
        feature_root(str): absolute path to feature location
        features(List[str]): relative path to features
    Returns:
        SUCCESS if every possible feautre is loaded successfull else FAILURE
    """
    ret = 0
    for item in features:
        path = join(feature_root, item + '.py')
        ret += load_module(path, FEATURE_PATH_PACKAGE)

    return ret


FEATURE_PATH_PACKAGE = 'rawmaker.features'
REQUIRED_METHODS = {'commandline', 'work'}


def load_module(path: str, sub_module: str):
    """Load feature and check the interface

    Args:
        path(str): absoulte path to feature
        sub_module(str): packagename of the featurelocation, see
                         FEATURE_PATH_PACKAGE
    Returns:
        SUCCESS if the feature provide all REQUIRED_METHODS else FAILURE
    """
    module_name = sub_module + '.' + basename(path)

    # load module from path
    spec = spec_from_file_location(module_name, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)

    # check the provision of all `REQUIRED_METHODS`
    methods = set(dir(module))
    if len(REQUIRED_METHODS & methods) == len(REQUIRED_METHODS):
        if not module_name in modules.keys():
            modules[module_name] = module
            logging('LOAD FEATURE: %s' % module.__name__)
        else:
            logging('SKIP LOADING: %s' % module.__name__)
        return SUCCESS
    else:
        missing_methods = REQUIRED_METHODS - methods

        for item in missing_methods:
            logging_error('MISSING METHOD %s in %s' % (item, module.__name__))
        logging_error('ABORT LOADING')
        return FAILURE
