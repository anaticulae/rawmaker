# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila
import utila.cli

import letty
import letty.quality.whitespace


@utila.saveme
def main() -> int:
    commands = [
        utila.cli.Flag('--whitespace', message='evalute number of whitespaces'),
    ]
    parser = utila.cli.create_parser(
        todo=commands,
        config=utila.ParserConfiguration(
            inputparameter=True,
            outputparameter=False,
            pages=True,
            prefix=False,
            verboseflag=True,
        ),
        version=letty.__version__,
        prog=letty.PROCESS,
    )
    args = utila.parse(parser)  # pylint:disable=W0612

    inpath, _ = utila.cli.sources(args, singleinput=True)
    inpath = inpath[0]
    if args['whitespace']:
        pages = None
        if args['pages'] is not None:
            pages = utila.parse_pages(','.join(args['pages']))
        whitespaces = letty.quality.whitespace.determine(inpath, pages=pages)
        utila.log(whitespaces)
        return utila.SUCCESS
    parser.print_help()
    return utila.FAILURE
