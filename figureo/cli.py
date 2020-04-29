# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utila
import utila.cli

import figureo
import figureo.data
import figureo.extract


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

    inpath, outpath = utila.cli.sources(args, singleinput=True)
    inpath = inpath[0]
    if not os.path.isfile(inpath):
        utila.error(f'require pdf file: {inpath}')
        return utila.FAILURE

    pages = None
    if args['pages'] is not None:
        pages = utila.parse_pages(','.join(args['pages']))

    extracted = figureo.extract.extract_figures(inpath, pages=pages)
    if extracted:
        os.makedirs(outpath, exist_ok=True)
        utila.log(f'write {len(extracted)} figures')
        figureo.data.dump_figures(extracted, outpath)
    return utila.SUCCESS
