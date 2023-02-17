# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila
import utila.cli

import letty
import letty.quality.whitespace


@utila.saveme
def main() -> int:
    parser = create_parser()
    args = utila.parse(parser)  # pylint:disable=W0612
    inpath, pages, whitespace = parse_args(args)
    if whitespace:
        white_spaces = letty.quality.whitespace.determine(inpath, pages=pages)
        utila.log(white_spaces)
        return utila.SUCCESS
    parser.print_help()
    return utila.FAILURE


def parse_args(args) -> tuple:
    """\
    >>> parse_args({})
    ('...', None, False)
    >>> parse_args(dict(pages=['3:10']))
    ('...', (3, 4, 5, 6, 7, 8, 9), False)
    """
    inpath, _ = utila.cli.sources(args, singleinput=True)  # pylint:disable=W0632
    inpath = inpath[0]
    pages = None
    if args.get('pages', None) is not None:
        pages = utila.parse_pages(','.join(args['pages']))
    whitespace = args.get('whitespace', False)
    result = (inpath, pages, whitespace)
    return result


def create_parser():
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
    return parser
