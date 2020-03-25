# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila
import utila.cli

import letty


@utila.saveme
def main():
    commands = [
        utila.cli.Flag(
            '--whitespaces', message='evalute number of whitespaces'),
    ]
    parser = utila.cli.create_parser(
        todo=commands,
        config=utila.ParserConfiguration(
            outputparameter=True,
            inputparameter=True,
            prefix=False,
        ),
        version=letty.__version__,
        prog=letty.PROCESS,
    )
    args = utila.parse(parser)  # pylint:disable=W0612
