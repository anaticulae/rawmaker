# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================


import sys

import utila

import rawmaker.cleanup.work

PROCESS = 'rawmaker_cleanup'
DESCRIPTION = """\
Load PageTextNavigators, codes, figures and tables.

It removes text which is inside codes, figures and or tables and writes
PageTextNavigators afterwards.
"""


@utila.saveme
def main():
    parameter = user_input()
    rawmaker.cleanup.work.cleanup(*parameter)
    sys.exit(utila.SUCCESS)


def user_input() -> tuple:
    todo = [
        utila.Flag(longcut='backup', message='write copy of source data'),
        utila.Parameter(longcut='postfix', message='rename output'),
    ]
    parser = utila.cli.create_parser(
        todo=todo,
        config=utila.ParserConfiguration(
            inputparameter=True,
            outputparameter=True,
            multiprocessed=False,
            pages=True,
            prefix=True,
            verboseflag=True,
            waitingflag=False,
            cacheflag=False,
        ),
        version=rawmaker.__version__,
        prog=PROCESS,
    )
    args = utila.parse(parser)
    choice = (
        args['input'],
        args['output'],
        args['prefix'],
        args['postfix'],
        utila.parse_pages(','.join(args['pages'])),  # DIRTY
        args['backup'],
    )
    return choice
