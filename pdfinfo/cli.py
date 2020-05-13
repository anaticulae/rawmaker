# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
import os

import utila
import utila.cli

import pdfinfo
import pdfinfo.data
import rawmaker.error

DESCRIPTION = """\
Verify given -i input file that file is a valid pdf file. Extract:
 + version
 + generator
 + pages

If no output is given, print validation result to stdout.
"""

@utila.saveme
def main():
    commands = [
        utila.cli.Flag(
            '--status',
            message=('evaluate pdfinfo.json. '
                     'return 0 if info is valid, 4 if pdfinfo is invalid, '
                     '2 if pdfinfo does not exists')),
    ]
    parser = utila.cli.create_parser(
        config=utila.ParserConfiguration(
            outputparameter=True,
            inputparameter=True,
            prefix=False,
        ),
        description=DESCRIPTION,
        todo=commands,
        version=pdfinfo.__version__,
    )
    args = utila.parse(parser)
    inpath, outpath = utila.sources(args, singleinput=True)
    # we support only a single path, just run the program more than one if
    # you want more.
    inpath = inpath[0]
    if args['status']:
        return status(inpath)

    # TODO: REPLACE AFTER UPGRADING UTILA
    if args['output'] is None:
        outpath = None
    validated = validate(inpath, outpath)
    return validated


def validate(inpath, outpath) -> int:
    if not os.path.isfile(inpath):
        utila.error(f'require valid file resource: {inpath}')
        return utila.INVALID_COMMAND
    assert os.path.exists(inpath), f'invalid inpath: {inpath}'

    try:
        parsed = pdfinfo.data.parse(inpath)
    except rawmaker.error.InvalidPDF:
        # not a valid pdf file
        parsed = None

    jsonify = '{}'
    if parsed is not None:
        jsonify = pdfinfo.data.jsonify(parsed)

    if outpath is None:
        # print to stdout
        utila.log(jsonify)
    else:
        if outpath is not None and os.path.isdir(outpath):
            outpath = os.path.join(outpath, 'pdfinfo.json')
        utila.file_replace(outpath, jsonify)
    return utila.SUCCESS


def status(path: str) -> int:
    source = os.path.join(path, 'pdfinfo.json')
    if not os.path.exists(source):
        utila.error(f'path: {source} does not exists')
        return utila.INVALID_COMMAND

    parsed = utila.file_read(source)
    if parsed == '{}':
        return pdfinfo.INVALID_PDF
    return utila.SUCCESS
