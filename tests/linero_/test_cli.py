# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

import tests.linero_


@pytest.mark.parametrize('command', [
    '--help',
])
def test_linero_cli_run(command, td, mp):  #pylint: disable=W0613
    """Run help and version and format command to reach basic test coverage"""
    tests.linero_.run(command, mp=mp)
