# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
from utila import Flag
from utila import logging
from utila import logging_error

from rawmaker.features import process_pagecontent


# TODO: Remove after upgrading iamraw
@classmethod
def from_list(cls, data):
    """Create Box from list"""
    return cls(
        x_bottom=data[0],
        y_bottom=data[1],
        x_top=data[2],
        y_top=data[3],
    )


def work(document):
    return {'feature_box': ''}


def commandline():
    return Flag(longcut='%s' % name(), message='Extract boxes out of document.')


def name():
    return 'boxes'
