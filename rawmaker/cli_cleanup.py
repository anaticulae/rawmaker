# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import argparse
import os
import sys

import utila

PROCESS = 'rawmaker_cleanup'
DESCRIPTION = """\
Load PageTextNavigators, figures and tables.

It removes text which is inside figures and or tables and writes
PageTextNavigators afterwards.
"""


@utila.saveme
def main():
    parameter = user_input()
    sys.exit(utila.SUCCESS)


def user_input() -> tuple:
    parser = argparse.ArgumentParser(
        prog=PROCESS,
        description=DESCRIPTION,
    )
    parser.add_argument(
        '-i',
        dest='inpath',
        default=os.getcwd(),
    )
    parser.add_argument(
        '-o',
        dest='outpath',
        default=os.path.join(os.getcwd(), 'outpath'),
    )
    parser.add_argument(
        '--prefix',
        dest='prefix',
        default='',
    )
    parser.add_argument(
        '--postfix',
        dest='postfix',
        default='',
    )
    args = parser.parse_args()
    choice = args.inpath, args.outpath, args.prefix, args.postfix
    return choice
