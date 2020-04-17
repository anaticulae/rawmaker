# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila
import utila.cli

import figureo


@utila.saveme
def main() -> int:
    commands = []
    parser = utila.cli.create_parser(
        todo=commands,
        config=utila.ParserConfiguration(
            outputparameter=True,
            inputparameter=True,
            prefix=False,
            pages=True,
        ),
        version=figureo.__version__,
        prog=figureo.PROCESS,
    )
    args = utila.parse(parser)  # pylint:disable=W0612

    inpath, _ = utila.cli.sources(args, singleinput=True)
    inpath = inpath[0]
    pages = None
    if args['pages'] is not None:
        pages = utila.parse_pages(args['pages'])

    parser.print_help()
    return utila.FAILURE
