# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import utilatest

import rawmaker
import rawmaker.cleanup.cli

#pylint: disable=invalid-name
run = functools.partial(
    utilatest.run_command,
    main=rawmaker.cleanup.cli.main,
    process=rawmaker.cleanup.cli.PROCESS,
    success=True,
)

failure = functools.partial(
    utilatest.run_command,
    main=rawmaker.cleanup.cli.main,
    process=rawmaker.cleanup.cli.PROCESS,
    success=False,
)
