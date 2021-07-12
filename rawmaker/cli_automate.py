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
import utilatest

DESCRIPTION = """\
Collect pdf files of defined folders and use them to run rawmaker.
"""


@utila.saveme
def main():
    parameter = user_input()
    run(*parameter)
    sys.exit(utila.SUCCESS)


def user_input() -> tuple:
    parser = argparse.ArgumentParser(description=DESCRIPTION)
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
        '-n',
        default=1,
        type=int,
        dest='cores',
        help='count of used cores',
    )
    args = parser.parse_args()
    inpath, outpath, cores = args.inpath, args.outpath, args.cores
    return inpath, outpath, cores


def run(inpath: str, outpath: str, cores: int = 1):
    os.makedirs(outpath, exist_ok=True)
    files = utila.file_list(inpath, include='pdf', absolute=True)
    for item in files:
        utila.log(item)
    cmds = []
    for item in files:
        _, name = os.path.split(item)
        # use quotation marks to encapsulate file path white spaces
        item = f'"{item}"' if ' ' in str(item) else item
        name = utilatest.simple(name)  # TODO: REPLACE WITH UTILA CODE
        out = os.path.join(outpath, name)
        cmd = f'rawmaker -i {item} -o {out} -j4'
        cmds.append(cmd)
    for cmd in cmds:
        utila.log(cmd, forwardnewline=False)
    utila.run_parallel(cmds, worker=cores, verbose=True)
