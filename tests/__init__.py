#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import functools

import pytest
import utilatest

from rawmaker import PROCESS_NAME
from rawmaker import ROOT
from rawmaker.cli import main
from tests.resources import RESOURCES

#pylint: disable=invalid-name
run = functools.partial(
    utilatest.run_command,
    main=main,
    process=PROCESS_NAME,
    success=True,
)

failure = functools.partial(
    utilatest.run_command,
    main=main,
    process=PROCESS_NAME,
    success=False,
)

skip_virtual = pytest.mark.skipif(
    not utilatest.NONVIRTUAL,
    reason="require non virtual environment",
)

# TODO: CONVERT TO PYTEST PLUGIN
SETUP_LONGRUN = f"""
uninstall rawmaker

install {ROOT}

run power --all {RESOURCES}
"""
