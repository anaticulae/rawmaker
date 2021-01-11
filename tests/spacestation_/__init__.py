# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import utilatest

import spacestation
import spacestation.cli

run = functools.partial(  # pylint:disable=C0103
    utilatest.run_command,
    main=spacestation.cli.main,
    process=spacestation.PROCESS,
    success=True,
)

failure = functools.partial(  # pylint:disable=C0103
    utilatest.run_command,
    main=spacestation.cli.main,
    process=spacestation.PROCESS,
    success=False,
)
