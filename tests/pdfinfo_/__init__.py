# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import utila

import pdfinfo
import pdfinfo.cli

run_success = functools.partial(  # pylint:disable=C0103
    utila.run_command,
    main=pdfinfo.cli.main,
    process=pdfinfo.PROCESS,
    success=True,
)

run_failure = functools.partial(  # pylint:disable=C0103
    utila.run_command,
    main=pdfinfo.cli.main,
    process=pdfinfo.PROCESS,
    success=False,
)
