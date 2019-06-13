# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pdfminer.layout import LAParams
from utila import FAILURE
from utila import logging_error


def create_layout(parameter):
    char_margin = get(parameter, 'char_margin', default=5.0, min_value=0.1)
    # boxes_flow: 1.0 only the vertical position matters
    result = LAParams(char_margin=char_margin, boxes_flow=1.0)
    return result


def get(args, parameter: str, default, min_value=None):
    value = None
    try:
        # TODO: inherit type from default, search for pythonic way
        value = default if args[parameter] is None else float(args[parameter])
    except KeyError:
        value = default

    if min_value is not None and value < min_value:
        logging_error('%s %.2f is to little' % (parameter, value))
        exit(FAILURE)
    return value
