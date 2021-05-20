# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
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

COMMANDS = [
    utila.cli.Flag(
        '--status',
        message=('evaluate pdfinfo.json. '
                 'return 0 if info is valid, 4 if pdfinfo is invalid, '
                 '2 if pdfinfo does not exists')),
    utila.cli.Command(
        longcut='--format',
        message='choose output format, json is default',
        args={
            'nargs': '?',
            'const': 'auto',
            'choices': [
                'json',
                'yaml',
            ],
        },
    ),
    utila.cli.Flag('--strict', message='fail on invalid pdf file'),
]

CONFIG = utila.ParserConfiguration(
    inputparameter=True,
    outputparameter=True,
    prefix=False,
    verboseflag=True,
    multiprocessed=False,
    pages=False,
    cacheflag=False,
)


@utila.saveme
def main():
    parser = utila.cli.create_parser(
        config=CONFIG,
        description=DESCRIPTION,
        todo=COMMANDS,
        version=pdfinfo.__version__,
    )
    args = utila.parse(parser)
    inpath, outpath = utila.sources(args, singleinput=True) # pylint:disable=W0632
    # It is only single path supported. Run program multiple times if more
    # than one analysis is required.
    inpath = inpath[0]
    if args['status']:
        return status(inpath)
    # TODO: REPLACE AFTER UPGRADING UTILA
    if args['output'] is None:
        outpath = None
    ext = args['format']
    if ext is None:
        ext = 'json'
    strict = args.get('strict', False)
    validated = validate(inpath, outpath, ext, strict)
    return validated


def validate(inpath, outpath, ext='json', strict: bool = False) -> int:
    if not os.path.isfile(inpath):
        utila.error(f'require valid pdf file: {inpath}')
        return utila.INVALID_COMMAND
    assert os.path.exists(inpath), f'invalid inpath: {inpath}'
    try:
        parsed = pdfinfo.data.parse(inpath)
    except rawmaker.error.InvalidPDF:
        # not a valid pdf file
        parsed = None
    if parsed is None and strict:
        utila.error(f'invalid pdf file: {inpath}')
        return pdfinfo.INVALID_PDF
    raw = '{}'
    if parsed is not None:
        raw = pdfinfo.data.dump(parsed, ext)
    if outpath is None:
        # print to stdout
        utila.log(raw)
    else:
        if os.path.isdir(outpath):
            outpath = os.path.join(outpath, f'pdfinfo.{ext}')
        assert str(outpath).endswith(
            ext), f'missmatching --format and --outpath {outpath}'
        utila.file_replace(outpath, raw)
    return utila.SUCCESS


def status(path: str) -> int:
    source = os.path.join(path, 'pdfinfo.json')
    if not os.path.exists(source):
        utila.error(f'path: {source} does not exists')
        return utila.INVALID_COMMAND
    # load status
    parsed = utila.file_read(source)
    if parsed == '{}':
        return pdfinfo.INVALID_PDF
    return utila.SUCCESS
