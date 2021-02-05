#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import functools

import pytest
import utilatest

import tests.resources
from rawmaker import PROCESS
from rawmaker import ROOT
from rawmaker.cli import main

#pylint: disable=invalid-name
run = functools.partial(
    utilatest.run_command,
    main=main,
    process=PROCESS,
    success=True,
)

failure = functools.partial(
    utilatest.run_command,
    main=main,
    process=PROCESS,
    success=False,
)

security = utilatest.register_marker('security')
font = utilatest.register_marker('font')
