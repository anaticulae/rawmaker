# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import utila

import linero
import linero.cli

run_success = functools.partial(  # pylint:disable=C0103
    utila.run_command,
    main=linero.cli.main,
    process=linero.PROCESS,
    success=True,
)

run_failure = functools.partial(  # pylint:disable=C0103
    utila.run_command,
    main=linero.cli.main,
    process=linero.PROCESS,
    success=False,
)
