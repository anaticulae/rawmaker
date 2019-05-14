# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
from utila import Flag


def work(document):
    return {'feature_box': ''}


def commandline():
    return Flag(longcut='%s' % name(), message='Extract boxes out of document.')


def name():
    return 'boxes'
